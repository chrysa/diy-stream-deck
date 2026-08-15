# Deep-dive — `chrysa/diy-stream-deck`

**Purpose (1 phrase).** Alternative open-source au Stream Deck Elgato, cross-platform Linux/Windows, qui mappe des entrées physiques (macropad USB, Raspberry Pi Pico W, tablette recyclée) vers des actions configurables en YAML (service Home Assistant, commande shell, requête HTTP, contrôle média, raccourci clavier).

**État réel du repo.** Scaffold précoce : seul `diy_stream_deck/__main__.py` (entrée CLI `python -m diy_stream_deck --config <file>` + `--dry-run`) existe. L'archi `core/ actions/ hardware/ config/ ui/` est **cible**, pas encore écrite. Stack : Python 3.14, `pyyaml`, `requests`, `pynput` (Windows/global HID), `evdev` (extra linux), ruff strict + mypy strict, coverage ≥ 85 %. Licence : **MIT**.

Le domaine « stream deck alternative » est très fourni en OSS ; les patterns ci-dessous couvrent les 5 briques manquantes : abstraction HID, boucle event→action, plugin d'actions, intégration Home Assistant, et device virtuel de test.

---

## 1. abcminiuser/python-elgato-streamdeck — abstraction HID multi-backend

- **owner/repo** : `abcminiuser/python-elgato-streamdeck`
- **stars** : 1 125 · **activité** : push 2026-08-10 (très actif) · **langage** : Python
- **licence** : permissive style MIT/X11 (« Permission to use, copy, modify, and distribute … granted without fee ») — GitHub la classe `NOASSERTION` mais le texte est **copiable** (équivalent MIT). ✅
- **fichier/module du pattern** : `src/StreamDeck/Transport/` (backends `HIDAPI`, `HID`, `Dummy`) + `src/StreamDeck/DeviceManager.py`
- **mécanisme réel** : une couche `Transport` abstraite avec plusieurs backends HID concrets (hidapi C, `hid` pur, dummy pour test) sélectionnés à l'exécution ; `DeviceManager.enumerate()` renvoie des objets device homogènes quel que soit l'OS. C'est exactement le pattern « hardware abstraction layer » que le README de diy-stream-deck décrit comme cible.
- **snippet portable** (structure du HAL, à réécrire — inspiration du design, pas copie) :

```python
# hardware/base.py
from abc import ABC, abstractmethod
from collections.abc import Iterator

class InputDevice(ABC):
    @abstractmethod
    def open(self) -> None: ...
    @abstractmethod
    def read_events(self) -> Iterator[int]:  # yields key indices
        ...
    @abstractmethod
    def close(self) -> None: ...

class DeviceManager:
    def __init__(self) -> None:
        self._backends: list[type[InputDevice]] = []
    def register(self, backend: type[InputDevice]) -> None:
        self._backends.append(backend)
    def enumerate(self) -> list[InputDevice]:
        return [b() for b in self._backends]  # each backend probes its own bus
```

- **étapes d'intégration** : (1) créer `diy_stream_deck/hardware/base.py` avec `InputDevice` ABC + `DeviceManager` ; (2) backends concrets `evdev_device.py` (Linux), `pynput_device.py` (Windows), `virtual_device.py` (test) ; (3) sélection par plateforme via `sys.platform`, import conditionnel comme le mandate CLAUDE.md.
- **gotchas** : leur API vise des devices Elgato *à écran* (images sur boutons) — diy-stream-deck vise des macropads/HID génériques, donc ne pas copier la partie image/ImageHelpers. Le backend `hid` exige libhidapi natif ; garder `evdev`/`pynput` (déjà choisis) plutôt que d'ajouter cette dépendance.

---

## 2. StreamController/StreamController — architecture de plugins d'actions

- **owner/repo** : `StreamController/StreamController`
- **stars** : 1 084 · **activité** : push 2026-08-15 (très actif) · **langage** : Python
- **licence** : **GPL-3.0** — copyleft. ⚠️ **RÉIMPLÉMENTER** : ne pas copier de code, s'inspirer de la conception uniquement.
- **fichier/module du pattern** : `src/backend/PluginManager/ActionBase.py` + `ActionHolder.py` — chaque action est une classe héritant d'`ActionBase` avec hooks `on_key_down` / `on_ready`, découverte dynamique des plugins.
- **mécanisme réel** : un registre charge dynamiquement des sous-classes d'`ActionBase` ; la config référence une action par identifiant ; le runner instancie et appelle `on_key_down`. C'est le modèle « actions pluggable et testables indépendamment » exigé par CLAUDE.md.
- **snippet portable** (réécriture propre, registre par décorateur) :

```python
# actions/base.py
from abc import ABC, abstractmethod

class Action(ABC):
    id: str  # e.g. "ha_service", "shell_cmd"
    @abstractmethod
    def run(self, params: dict) -> None: ...

_REGISTRY: dict[str, type[Action]] = {}

def register(cls: type[Action]) -> type[Action]:
    _REGISTRY[cls.id] = cls
    return cls

def build(action_id: str) -> Action:
    return _REGISTRY[action_id]()
```

- **étapes d'intégration** : (1) `actions/base.py` avec `Action` ABC + registre ; (2) une classe par action (`HaServiceAction`, `ShellCmdAction`, `HttpRequestAction`, `MediaControlAction`, `HotkeyAction`), chacune `@register` ; (3) le key mapper résout `key → action_id + params` depuis le YAML et appelle `build(id).run(params)`.
- **gotchas** : GPL — se limiter au concept (ABC + registre), design trivial et non protégeable, mais ne lire aucun bloc de leur code pour l'écrire. Éviter leur couplage à GTK/GLib (app Linux à écran) ; garder les actions headless et sans I/O au constructeur pour rester testables.

---

## 3. TheBeachLab/stream-deck — grab exclusif d'un clavier via evdev (Linux)

- **owner/repo** : `TheBeachLab/stream-deck`
- **stars** : 30 · **activité** : push 2020-10-12 (dormant) · **langage** : Python
- **licence** : repo **GPL-3.0** (l'en-tête du fichier dit « MIT » — incohérence ; le fichier LICENSE fait foi → traiter en **GPL/RÉIMPLÉMENTER**). ⚠️
- **fichier/module du pattern** : `autohotkey.py` — `InputDevice(path)` + `dev.grab()` pour capter un clavier secondaire, boucle `for ev in dev.read_loop()` → `subprocess.Popen`.
- **mécanisme réel** : ouvre `/dev/input/by-id/usb-…-event-kbd`, appelle `.grab()` pour empêcher le clavier de taper dans le système, filtre les key-down et lance des programmes. C'est la brique Linux HID (backend `evdev`) que diy-stream-deck doit fournir.
- **snippet portable** (technique standard evdev, réécrite) :

```python
# hardware/evdev_device.py  (Linux; extra "linux")
from evdev import InputDevice, categorize, ecodes

def read_keys(device_path: str):
    dev = InputDevice(device_path)
    dev.grab()               # exclusive: macropad frappes n'atteignent pas le desktop
    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                k = categorize(event)
                if k.keystate == k.key_down:
                    yield k.scancode
    finally:
        dev.ungrab()
```

- **étapes d'intégration** : implémenter le backend Linux du HAL (source 1) avec ce `read_loop`/`grab` ; le device path vient du YAML ou d'une auto-détection `by-id`.
- **gotchas** : `grab()` nécessite l'appartenance au groupe `input` (droits /dev/input) ; toujours `ungrab()` en `finally` sinon le clavier reste séquestré après crash ; `read_loop()` est bloquant → l'exécuter dans un thread/async à part de la boucle principale. Le pattern est trivial et non protégeable, mais le repo étant GPL, écrire depuis la doc evdev, pas depuis leur fichier.

---

## 4. willianrod/ODeck — device « virtuel » réseau (tablette/téléphone comme deck)

- **owner/repo** : `willianrod/ODeck`
- **stars** : 440 · **activité** : push 2024-02-17 (peu actif) · **langage** : TypeScript (Electron)
- **licence** : **MIT** — copiable ✅ (concept ; le code TS n'est pas directement portable en Python).
- **fichier/module du pattern** : serveur `src/main` exposant un endpoint que le client mobile appelle → un « bouton » distant déclenche une action locale. Couvre le form-factor « tablette recyclée » listé dans le README de diy-stream-deck.
- **mécanisme réel** : le device physique est remplacé par un client réseau ; le daemon héberge un petit serveur (WebSocket/HTTP) et chaque appui envoie `{key_id}` traité par le même key mapper que les entrées HID.
- **snippet portable** (backend virtuel = source d'événements réseau, aligné sur le HAL source 1) :

```python
# hardware/virtual_device.py — deck depuis une tablette via HTTP POST /press
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, queue

def serve_virtual_deck(host: str, port: int, events: "queue.Queue[int]") -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            events.put(int(body["key"]))   # même flux que evdev/pynput
            self.send_response(204); self.end_headers()
    HTTPServer((host, port), Handler).serve_forever()
```

- **étapes d'intégration** : ajouter `VirtualDevice` au `DeviceManager` ; il alimente la même file d'événements que les backends HID → réutilise tout le pipeline mapper/actions. Sert aussi de device de test sans matériel (exigence CLAUDE.md « virtual device for testing »).
- **gotchas** : exposer sur `127.0.0.1` par défaut (un deck réseau ouvert = surface d'attaque) ; ajouter un token si bind hors-loopback. Ne pas porter le code Electron ; ne garder que l'idée client-réseau→événement.

---

## 5. Home Assistant REST API — action `ha_service` (intégration native)

- **owner/repo** : `home-assistant/core` (référence de l'API ; la doc `developers.home-assistant.io/docs/api/rest`)
- **stars** : ~ (projet majeur, très actif) · **licence** : **Apache-2.0** — copiable ✅ ; ici on consomme juste l'API REST (pas de code à copier).
- **fichier/module du pattern** : endpoint `POST /api/services/<domain>/<service>` avec bearer token — c'est le mécanisme d'appel de service HA.
- **mécanisme réel** : requête HTTP authentifiée par long-lived access token ; corps JSON = `entity_id` + data du service. `requests` (déjà en dépendance) suffit, aucune lib HA requise → respecte « HA optional, never required to start ».
- **snippet portable** :

```python
# actions/ha_service.py
import requests
from actions.base import Action, register

@register
class HaServiceAction(Action):
    id = "ha_service"
    def run(self, params: dict) -> None:
        base, token = params["base_url"], params["token"]
        domain, service = params["service"].split(".", 1)  # "light.turn_on"
        requests.post(
            f"{base}/api/services/{domain}/{service}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=params.get("data", {}),
            timeout=5,
        ).raise_for_status()
```

- **étapes d'intégration** : (1) action enregistrée dans le registre (source 2) ; (2) le YAML porte `base_url`/`token` (via env/secret, pas en clair) ; (3) rendre l'échec non-fatal (log + continue) pour ne jamais bloquer le daemon si HA est down.
- **gotchas** : token long-lived = secret → jamais dans le YAML committé, lire depuis env ou fichier secret ; toujours `timeout=` (HA injoignable ne doit pas figer la boucle d'actions) ; mettre l'appel réseau hors thread principal si la boucle HID est synchrone.

---

## Synthèse licences

| Source | Licence | Verdict |
| --- | --- | --- |
| abcminiuser/python-elgato-streamdeck | MIT/X11-style (NOASSERTION) | ✅ copiable |
| willianrod/ODeck | MIT | ✅ copiable (concept) |
| home-assistant/core (API REST) | Apache-2.0 | ✅ copiable |
| StreamController | **GPL-3.0** | ⚠️ réimplémenter (concept seul) |
| TheBeachLab/stream-deck | **GPL-3.0** (en-tête dit MIT, incohérent) | ⚠️ réimplémenter |

**Priorité d'intégration** (quick-wins d'abord) : (1) HAL `DeviceManager`/`InputDevice` + backend `virtual` (source 1+4, testable sans matériel, débloque tout le reste) → (2) registre d'actions + `ha_service`/`shell_cmd` (source 2+5) → (3) backend `evdev` réel (source 3).
