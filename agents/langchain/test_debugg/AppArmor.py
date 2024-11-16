import os
import subprocess

APPARMOR_PROFILE = """
#include <tunables/global>

/usr/bin/agent {
    capability sys_admin,
    capability net_admin,

    /path/to/agent/** rix,
    /path/to/logs/** rw,

    network inet stream,
    network inet6 stream,

    deny /home/** rw,
    deny /etc/** rw,
    deny /usr/** rwk,
}
"""

def setup_apparmor():
    profile_path = "/etc/apparmor.d/usr.bin.agent"
    try:
        # Write the AppArmor profile
        with open(profile_path, "w") as f:
            f.write(APPARMOR_PROFILE)

        # Reload and enforce the profile
        subprocess.run(["apparmor_parser", "-r", profile_path], check=True)
        subprocess.run(["aa-enforce", "/usr/bin/agent"], check=True)
        print("AppArmor profile successfully applied.")
    except Exception as e:
        print(f"Error setting up AppArmor: {e}")

if __name__ == "__main__":
    setup_apparmor()
