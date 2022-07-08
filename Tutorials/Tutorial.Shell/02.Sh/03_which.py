import sh

has_ansible = sh.which("ansible") is not None
if not has_ansible:
    print("You should install ansible.")
