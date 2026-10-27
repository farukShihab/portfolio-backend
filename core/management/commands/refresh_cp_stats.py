import os
from django.core.management.base import BaseCommand
from core.models import PlatformStats
from core import cp_fetchers as f

PLATFORMS = {
    "codeforces": ("CF_HANDLE", f.codeforces),
    "atcoder":    ("ATCODER_HANDLE", f.atcoder),
    "leetcode":   ("LEETCODE_HANDLE", f.leetcode),
}

class Command(BaseCommand):
    help = "Fetch CP stats and cache them in PlatformStats"

    def handle(self, *args, **opts):
        for name, (env, fetch) in PLATFORMS.items():
            handle = os.getenv(env)
            if not handle:
                self.stderr.write(f"skip {name}: {env} not set")
                continue
            try:
                data = fetch(handle)
                PlatformStats.objects.update_or_create(
                    platform=name, defaults={"handle": handle, **data})
                self.stdout.write(self.style.SUCCESS(f"{name}: {data['solved']} solved"))
            except Exception as e:
                self.stderr.write(f"{name} failed, keeping old data: {e}")