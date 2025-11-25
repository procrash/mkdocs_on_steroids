"""
MkDocs Build Control Hook
==========================
Prüft vor jedem Build, ob der Build pausiert werden soll.

Wenn die Datei '.mkdocs-build-paused' existiert, wird der Build übersprungen.
Dies ermöglicht es, vom Browser aus den HTML-Build zu pausieren,
während die LLM-Dokumentations-Generierung weiterläuft.
"""

from pathlib import Path
import logging
import sys

logger = logging.getLogger('mkdocs.hooks.build_control')

BUILD_PAUSE_FLAG = Path('.mkdocs-build-paused')


class BuildPausedException(Exception):
    """Exception, die geworfen wird, wenn der Build pausiert ist"""
    pass


def on_pre_build(config, **kwargs):
    """
    Hook, der vor jedem Build ausgeführt wird.

    Wenn die Pause-Flag-Datei existiert, wird der Build abgebrochen.
    Dies verhindert, dass HTML-Dateien neu gebaut werden, während
    die LLM-Dokumentations-Generierung im Hintergrund weiterläuft.
    """
    if BUILD_PAUSE_FLAG.exists():
        logger.warning("")
        logger.warning("=" * 70)
        logger.warning("⏸️  HTML-BUILD PAUSIERT")
        logger.warning("=" * 70)
        logger.warning("  📝 LLM-Dokumentations-Generierung läuft weiter im Hintergrund")
        logger.warning("  🚫 HTML-Dateien werden nicht aktualisiert")
        logger.warning("  ▶️  Klicke auf den Toggle-Button (🔨) im Browser zum Fortsetzen")
        logger.warning("  📄 Flag-Datei: .mkdocs-build-paused")
        logger.warning("=" * 70)
        logger.warning("")

        # Setze Marker für andere Hooks
        config['_build_paused'] = True

        # Verhindere den Build durch Exit
        # Dies ist die sauberste Methode, da MkDocs serve den Server
        # weiterlaufen lässt und nur den Build-Prozess beendet
        sys.exit(0)
    else:
        config['_build_paused'] = False
        logger.info("🟢 HTML-Build aktiviert - Dokumentation wird aktualisiert")


def on_files(files, config, **kwargs):
    """
    Hook, der die Dateiliste manipulieren kann.

    Wenn der Build pausiert ist, geben wir eine leere Dateiliste zurück,
    sodass nichts gebaut wird. Dies ist ein Fallback, falls on_pre_build
    nicht ausreichend ist.
    """
    if config.get('_build_paused', False):
        logger.debug("Build pausiert - keine Dateien werden verarbeitet")
        # Rückgabe einer leeren Files-Collection würde funktionieren,
        # aber wir verlassen uns auf sys.exit(0) in on_pre_build
        return files
    return files


def on_post_build(config, **kwargs):
    """
    Hook nach dem Build.

    Wird nur ausgeführt, wenn der Build nicht pausiert war.
    """
    if not config.get('_build_paused', False):
        logger.info("✅ HTML-Build erfolgreich abgeschlossen")
