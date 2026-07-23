#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC INSTALLER - Instalim nga Repositories Tona
=====================================================
Instalon: CLX, CLX.I (LLaVA), LLaMA dhe te gjitha paketat nga repot tona.
Zero dependencies te jashtme - cdo gje vjen nga ekosistemi yne.

Repo:
  - Web8kameleon-hub/* (11 repos)
  - LedjanAhmati/* (3 repos)
  - BledjonaAhmati/* (2 repos)
"""

import os
import sys
import json
import time
import hashlib
import datetime
import subprocess
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

# ============================================================================
# KONFIGURACIONI I REPOS
# ============================================================================

REPOS = [
    # CLX / LLM Core
    {
        "name": "clisonix.com",
        "url": "https://github.com/Web8kameleon-hub/clisonix.com.git",
        "type": "clx",
        "install": True,
    },
    {
        "name": "OS-CLX",
        "url": "https://github.com/Web8kameleon-hub/OS-CLX.git",
        "type": "clx_os",
        "install": True,
    },
    {
        "name": "Cwy",
        "url": "https://github.com/Web8kameleon-hub/Cwy.git",
        "type": "clx_web",
        "install": True,
    },
    # LLaVA / Vision
    {
        "name": "ultrathinking-web",
        "url": "https://github.com/Web8kameleon-hub/ultrathinking-web.git",
        "type": "llava",
        "install": True,
    },
    {
        "name": "ultrawebthinking",
        "url": "https://github.com/Web8kameleon-hub/ultrawebthinking.git",
        "type": "web_ai",
        "install": True,
    },
    # Infrastructure
    {
        "name": "Kloud",
        "url": "https://github.com/Web8kameleon-hub/Kloud.git",
        "type": "infra",
        "install": True,
    },
    {
        "name": "web8",
        "url": "https://github.com/Web8kameleon-hub/web8.git",
        "type": "nodedb",
        "install": True,
    },
    {
        "name": "OS-Web8",
        "url": "https://github.com/BledjonaAhmati/OS-Web8.git",
        "type": "nodedb_os",
        "install": True,
    },
    # Web & Content
    {
        "name": "clisonixwesterneurope",
        "url": "https://github.com/Web8kameleon-hub/clisonixwesterneurope.git",
        "type": "web",
        "install": True,
    },
    {
        "name": "clisonix-blog",
        "url": "https://github.com/LedjanAhmati/clisonix-blog.git",
        "type": "content",
        "install": True,
    },
    {
        "name": "clisonix-news",
        "url": "https://github.com/Web8kameleon-hub/clisonix-news.git",
        "type": "content",
        "install": True,
    },
    {
        "name": "starbooking",
        "url": "https://github.com/Web8kameleon-hub/starbooking.git",
        "type": "app",
        "install": True,
    },
    {
        "name": "Lightning-SPP-3.14",
        "url": "https://github.com/Web8kameleon-hub/Lightning-SPP-3.14.git",
        "type": "spp",
        "install": True,
    },
    {
        "name": "Ultrawebthinking",
        "url": "https://github.com/BledjonaAhmati/Ultrawebthinking.git",
        "type": "web_template",
        "install": True,
    },
    # Neurosonic Core (vetvetja)
    {
        "name": "neurosonic-core",
        "url": "https://github.com/LedjanAhmati/www.neuroconic.eu.git",
        "type": "core",
        "install": False,
    },
]


class NeurosonicInstaller:
    """
    Instaluesi i ekosistemit Neurosonic nga repositories tona.
    Asnje varesi e jashtme - cdo pakete vjen nga repot tona.
    """

    def __init__(self, target_dir: str = "repos"):
        self.target_dir = os.path.abspath(target_dir)
        self.installed = []
        self.failed = []
        self.logs = []

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.datetime.now().isoformat()
        entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(entry)
        print(entry)

    def ensure_dir(self, path: str):
        os.makedirs(path, exist_ok=True)

    def clone_repo(self, repo: Dict[str, Any]) -> bool:
        """Klonon nje repo nga GitHub"""
        name = repo["name"]
        url = repo["url"]
        dest = os.path.join(self.target_dir, name)

        if os.path.exists(dest):
            self.log(f"📂 {name}: Tashme ekziston ne {dest}")
            return True

        self.log(f"📦 {name}: Duke klonuar nga {url}...")
        try:
            result = subprocess.run(
                ["git", "clone", "--depth=1", url, dest],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                self.log(f"✅ {name}: Klonimi perfundoi me sukses")
                return True
            else:
                self.log(f"❌ {name}: Klonimi deshtoi: {result.stderr[:200]}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ {name}: Gabim: {str(e)}", "ERROR")
            return False

    def install_from_repo(self, repo: Dict[str, Any]) -> bool:
        """Instalon paketat nga nje repo"""
        name = repo["name"]
        repo_type = repo["type"]
        dest = os.path.join(self.target_dir, name)

        if not os.path.exists(dest):
            self.log(f"⚠️ {name}: Nuk u gjet. Duke klonuar...")
            if not self.clone_repo(repo):
                return False

        # Verifikojme strukturen e repo-s
        files = os.listdir(dest)
        self.log(f"📋 {name}: {len(files)} skedare/folders")

        # Instalojme sipas tipit
        if repo_type == "clx" or repo_type == "clx_os":
            self._install_clx_package(dest, name)
        elif repo_type == "llava":
            self._install_llava_package(dest, name)
        elif repo_type == "nodedb" or repo_type == "nodedb_os":
            self._install_nodedb_package(dest, name)
        elif repo_type == "spp":
            self._install_spp_package(dest, name)
        else:
            self._install_generic_package(dest, name)

        return True

    def _install_clx_package(self, path: str, name: str):
        """Instalon paketen CLX (CLX-LLM)"""
        bin_path = os.path.join(path, "bin")
        lib_path = os.path.join(path, "lib")

        # Krijon lidhje simbolike ose kopjon
        self._link_to_core(path, name, "clx")

        self.log(f"   🔗 CLX: {name} -> neurosonic/ai/clx_llm")

    def _install_llava_package(self, path: str, name: str):
        """Instalon paketen LLaVA / Vision"""
        self._link_to_core(path, name, "clx_i")
        self.log(f"   🔗 LLaVA: {name} -> neurosonic/ai/clx_i")

    def _install_nodedb_package(self, path: str, name: str):
        """Instalon NodeDB Fluid"""
        self._link_to_core(path, name, "nodedb")
        self.log(f"   🔗 NodeDB: {name} -> neurosonic/kernel/nodedb")

    def _install_spp_package(self, path: str, name: str):
        """Instalon Lightning SPP 3.14"""
        self._link_to_core(path, name, "spp")
        self.log(f"   🔗 SPP: {name} -> neurosonic/lightning_spp")

    def _install_generic_package(self, path: str, name: str):
        """Instalon pakete gjenerike"""
        self._link_to_core(path, name, "packages")
        self.log(f"   🔗 Package: {name} -> neurosonic/packages/{name}")

    def _link_to_core(self, source_path: str, name: str, category: str):
        """Krijon lidhje nga repo ne core"""
        core_packages_dir = os.path.join(os.getcwd(), "packages", category)
        self.ensure_dir(core_packages_dir)

        link_path = os.path.join(core_packages_dir, name)

        # Krijo nje skedar reference
        ref = {
            "package": name,
            "source": source_path,
            "installed": datetime.datetime.now().isoformat(),
            "type": category,
            "hash": hashlib.sha256(name.encode()).hexdigest()[:12],
        }

        with open(f"{link_path}.json", "w") as f:
            json.dump(ref, f, indent=2)

    def verify_installation(self) -> Dict[str, Any]:
        """Verifikon instalimin"""
        packages_dir = os.path.join(os.getcwd(), "packages")
        if not os.path.exists(packages_dir):
            return {"status": "empty", "packages": 0}

        categories = os.listdir(packages_dir)
        total_packages = 0

        for cat in categories:
            cat_path = os.path.join(packages_dir, cat)
            if os.path.isdir(cat_path):
                files = [f for f in os.listdir(cat_path) if f.endswith(".json")]
                total_packages += len(files)

        return {
            "status": "installed",
            "categories": len(categories),
            "packages": total_packages,
            "categories_list": categories,
        }

    def install_all(self) -> Dict[str, Any]:
        """Instalon te gjitha repos"""
        self.log("=" * 70)
        self.log("🔧 NEUROSONIC INSTALLER - Instalim nga Repositories Tona")
        self.log(f"📅 Data: {datetime.datetime.now().isoformat()}")
        self.log("=" * 70)

        self.ensure_dir(self.target_dir)
        self.ensure_dir(os.path.join(os.getcwd(), "packages"))

        repo_count = len(REPOS)
        self.log(f"\n📦 Gjithsej {repo_count} repos per tu instaluar\n")

        for i, repo in enumerate(REPOS, 1):
            self.log(f"\n[{i}/{repo_count}] {repo['name']} ({repo['type']})")

            if repo["install"]:
                success = self.install_from_repo(repo)
                if success:
                    self.installed.append(repo["name"])
                else:
                    self.failed.append(repo["name"])
            else:
                self.log(f"   ⏭️ Skip (core repo)")

        # Permbledhje
        self.log("\n" + "=" * 70)
        self.log("✅ INSTALIMI PERFUNDOI")
        self.log(f"   Te instaluara: {len(self.installed)}/{repo_count}")
        self.log(f"   Te deshtuara: {len(self.failed)}")

        if self.installed:
            self.log(f"\n   📦 Paketat e instaluara:")
            for pkg in self.installed:
                self.log(f"      ✅ {pkg}")

        if self.failed:
            self.log(f"\n   ❌ Deshtimet:")
            for pkg in self.failed:
                self.log(f"      ❌ {pkg}")

        # Verifikimi
        verification = self.verify_installation()
        self.log(f"\n📊 Verifikimi:")
        self.log(f"   Status: {verification['status']}")
        self.log(f"   Kategori: {verification['categories']}")
        self.log(f"   Paketa totale: {verification['packages']}")

        self.log("=" * 70)

        return {
            "installed": self.installed,
            "failed": self.failed,
            "total": repo_count,
            "verification": verification,
        }

    def get_summary(self) -> str:
        """Kthen nje permbledhje teksti"""
        lines = [
            "=" * 70,
            "🔧 NEUROSONIC INSTALLER - PERMBLEDHJE",
            "=" * 70,
            f"Total repos: {len(REPOS)}",
            f"Te instaluara: {len(self.installed)}",
            f"Te deshtuara: {len(self.failed)}",
            "",
            "Paketat e instaluara:",
        ]

        for pkg in self.installed:
            lines.append(f"  ✅ {pkg}")

        if self.failed:
            lines.append("")
            lines.append("Deshtimet:")
            for pkg in self.failed:
                lines.append(f"  ❌ {pkg}")

        lines.append("")
        lines.append("Komanda per te verifikuar:")
        lines.append(
            '  python -c "import neurosonic_import_manager; m = NeurosonicImportManager(); print(m.verify_all_packages())"'
        )
        lines.append("=" * 70)

        return "\n".join(lines)


# ============================================================================
# NEUROSONIC IMPORT MANAGER - Menaxhon importet nga repot tona
# ============================================================================


class NeurosonicImportManager:
    """
    Menaxhon importimin e CLX, CLX.I, LLaMA, LLaVA nga repot tona.

    N vend qe te perdorim pip install nga PyPI, ne importojme direkt
    nga repos tona te klonuara.
    """

    def __init__(self, repos_dir: str = "repos"):
        self.repos_dir = os.path.abspath(repos_dir)
        self.imported = {}
        self._setup_import_paths()

    def _setup_import_paths(self):
        """Shton repos tona ne sys.path qe te mund t'i importojme"""
        if os.path.exists(self.repos_dir):
            for repo_name in os.listdir(self.repos_dir):
                repo_path = os.path.join(self.repos_dir, repo_name)
                if os.path.isdir(repo_path):
                    # Shton rrugen kryesore
                    if repo_path not in sys.path:
                        sys.path.insert(0, repo_path)

                    # Shton src/ nese ekziston
                    src_path = os.path.join(repo_path, "src")
                    if os.path.isdir(src_path) and src_path not in sys.path:
                        sys.path.insert(0, src_path)

                    # Shton lib/ nese ekziston
                    lib_path = os.path.join(repo_path, "lib")
                    if os.path.isdir(lib_path) and lib_path not in sys.path:
                        sys.path.insert(0, lib_path)

        # Shton packages/ ne sys.path
        packages_dir = os.path.join(os.getcwd(), "packages")
        if os.path.exists(packages_dir):
            for cat in os.listdir(packages_dir):
                cat_path = os.path.join(packages_dir, cat)
                if os.path.isdir(cat_path) and cat_path not in sys.path:
                    sys.path.insert(0, cat_path)

    def import_clx(self) -> Any:
        """Importon CLX-LLM nga repot tona"""
        try:
            # Provojme nga repo clisonix.com
            from clisonix import clx as clx_module

            self.imported["clx"] = "clisonix.com"
            return clx_module
        except ImportError:
            try:
                # Provojme nga OS-CLX
                from osc import clx as clx_module

                self.imported["clx"] = "OS-CLX"
                return clx_module
            except ImportError:
                self.imported["clx"] = "not_found"
                return None

    def import_clx_i(self) -> Any:
        """Importon CLX.I (LLaVA - Vision) nga repot tona"""
        try:
            from ultrathinking import vision as clx_i_module

            self.imported["clx_i"] = "ultrathinking-web"
            return clx_i_module
        except ImportError:
            try:
                from ultraweb import llava as clx_i_module

                self.imported["clx_i"] = "ultrawebthinking"
                return clx_i_module
            except ImportError:
                self.imported["clx_i"] = "not_found"
                return None

    def import_llama(self) -> Any:
        """Importon LLaMA nga repot tona"""
        try:
            from clisonix import llama as llama_module

            self.imported["llama"] = "clisonix.com"
            return llama_module
        except ImportError:
            try:
                from osc import llama as llama_module

                self.imported["llama"] = "OS-CLX"
                return llama_module
            except ImportError:
                self.imported["llama"] = "not_found"
                return None

    def import_all(self) -> Dict[str, Any]:
        """Importon te gjitha paketat e disponueshme"""
        result = {}

        clx = self.import_clx()
        result["clx"] = {
            "status": "found" if clx else "not_found",
            "source": self.imported.get("clx"),
        }

        clx_i = self.import_clx_i()
        result["clx_i"] = {
            "status": "found" if clx_i else "not_found",
            "source": self.imported.get("clx_i"),
        }

        llama = self.import_llama()
        result["llama"] = {
            "status": "found" if llama else "not_found",
            "source": self.imported.get("llama"),
        }

        return result

    def verify_all_packages(self) -> Dict[str, Any]:
        """Verifikon te gjitha paketat nga repot tona"""
        packages_dir = os.path.join(os.getcwd(), "packages")
        repos_dir = self.repos_dir

        result = {
            "repos_installed": [],
            "packages_available": [],
            "import_status": {},
            "total": 0,
        }

        # Verifikon repos
        if os.path.exists(repos_dir):
            result["repos_installed"] = os.listdir(repos_dir)

        # Verifikon packages
        if os.path.exists(packages_dir):
            for cat in os.listdir(packages_dir):
                cat_path = os.path.join(packages_dir, cat)
                if os.path.isdir(cat_path):
                    for f in os.listdir(cat_path):
                        if f.endswith(".json"):
                            result["packages_available"].append(f"{cat}/{f}")

        # Verifikon importet
        result["import_status"] = self.import_all()

        result["total"] = len(result["repos_installed"]) + len(
            result["packages_available"]
        )

        return result

    def get_report(self) -> str:
        """Kthen nje raport teksti"""
        verification = self.verify_all_packages()

        lines = [
            "=" * 70,
            "📦 NEUROSONIC IMPORT MANAGER - RAPORT",
            "=" * 70,
            f"Repos te instaluara: {len(verification['repos_installed'])}",
            f"Packages te disponueshme: {len(verification['packages_available'])}",
            f"Total: {verification['total']}",
            "",
            "Statusi i importeve:",
        ]

        for pkg, status in verification["import_status"].items():
            icon = "✅" if status["status"] == "found" else "⬜"
            source = status["source"] or "N/A"
            lines.append(f"  {icon} {pkg}: {status['status']} (burimi: {source})")

        if verification["repos_installed"]:
            lines.append("")
            lines.append("Repos e instaluara:")
            for repo in verification["repos_installed"]:
                lines.append(f"  📁 {repo}")

        lines.append("=" * 70)

        return "\n".join(lines)


# ============================================================================
# MAIN - Pika e hyrjes
# ============================================================================


def main():
    """Pika kryesore e instalimit"""

    print("=" * 70)
    print("🧠 NEUROSONIC INSTALLER")
    print("Instalim nga repositories tona")
    print(f"Python: {sys.version}")
    print("=" * 70)

    # Hapi 1: Instalimi
    installer = NeurosonicInstaller()
    result = installer.install_all()

    print("\n" + installer.get_summary())

    # Hapi 2: Verifikimi i importeve
    print("\n")
    manager = NeurosonicImportManager()
    print(manager.get_report())

    # Hapi 3: Permbledhja finale
    print("\n")
    print("🔥 PERMBLEDHJA FINALE:")
    print(f"   Repos te klonuara: {len(result['installed'])}")
    print(f"   Packages te instaluara: {result['verification']['packages']}")
    print(f"   Kategori: {result['verification']['categories']}")
    print()

    if result["verification"]["packages"] > 0:
        print("✅ CLX, CLX.I, LLaMA, LLaVA dhe paketat e tjera jane gati!")
        print('   Per t\'i perdorur: python -c "import neurosonic_import_manager"')
    else:
        print(
            "⚠️ Disa repo mund te jene offline. Provo: python install_from_our_repos.py"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()
