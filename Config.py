import subprocess
import os


def run_command(command):
    """
    Run a shell command and return the output.

    + How To Run:
        - nano setup_squid.py
        - chmod +x setup_squid.py
        - sudo python3 setup_squid.py
        - Enjoy!

    Version: 0.0
    Timestamp: R

    :param command: Command to run
    :return: Output of the command
    """
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')


def setup_squid():
    """
    Setup Squid proxy server on the local machine.
    """
    # Update the system
    print("Updating the system...")
    print(run_command('sudo apt-get update -y'))

    # Install Squid
    print("Installing Squid...")
    print(run_command('sudo apt-get install squid -y'))

    # Configure Squid
    print("Configuring Squid...")
    squid_config = """
    http_port 3128
    acl localnet src 10.0.0.0/8
    http_access allow localnet
    http_access allow localhost
    http_access deny all
    """
    with open('/tmp/squid.conf', 'w') as config_file:
        config_file.write(squid_config)

    print(run_command('sudo mv /tmp/squid.conf /etc/squid/squid.conf'))

    # Restart Squid
    print("Restarting Squid...")
    print(run_command('sudo systemctl restart squid'))

    # Configure firewall
    print("Configuring firewall...")
    firewall_rule = "sudo ufw allow 3128/tcp"
    print(run_command(firewall_rule))
    print(run_command('sudo ufw reload'))


if __name__ == "__main__":
    setup_squid()
