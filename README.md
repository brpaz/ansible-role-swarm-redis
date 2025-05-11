# Ansible Swarm Redis

> An Ansible role to deploy a Redis service to a Docker Swarm cluster.

## Requirements

- Docker installed on the target machine
- Docker Swarm initialized on the target machine
- An overlay network for the swarm services

## Installation

### Using Ansible Galaxy

You can install this role directly from Ansible Galaxy:

```bash
ansible-galaxy install brpaz.swarm_redis
```

### Using requirements.yml

For version-controlled, repeatable role installations, add to your `requirements.yml`:

```yaml
---
roles:
  - name: brpaz.swarm_redis
    version: v1.0.0  # Specify the version you want

collections:
  - name: community.docker
```

Then install with:

```bash
ansible-galaxy install -r requirements.yml
```

### Manual Installation

Alternatively, you can clone the repository directly:

```bash
# Create a roles directory if it doesn't exist
mkdir -p ~/.ansible/roles
# Clone the repository
git clone https://github.com/brpaz/ansible-role-swarm-redis.git ~/.ansible/roles/brpaz.swarm_redis
```

## Role Variables

This role includes the following variables for configuration:

| Variable                | Default Value               | Description                                          |
| ----------------------- | --------------------------- | ---------------------------------------------------- |
| `redis_version`         | `7.0.11`                    | Redis version to use                                 |
| `redis_image`           | `redis:{{ redis_version }}` | Redis Docker image                                   |
| `redis_port`            | `6379`                      | Port Redis will listen on                            |
| `redis_port_mode`       | `ingress`                   | Docker service publish mode (ingress or host)        |
| `redis_password`        | `""`                        | Password for Redis authentication (empty by default) |
| `redis_conf`            | See below                   | Redis configuration settings                         |
| `redis_networks`        | `[{name: "swarm_network"}]` | Docker swarm network configuration                   |
| `redis_conf_dir`        | `/etc/redis`                | Local directory for configs                          |
| `redis_service_name`    | `redis`                     | Name of the Redis service                            |
| `redis_cpu_requests`    | `0.1`                       | CPU resource requests                                |
| `redis_cpu_limits`      | `0.5`                       | CPU resource limits                                  |
| `redis_memory_requests` | `32M`                       | Memory resource requests                             |
| `redis_memory_limits`   | `1G`                        | Memory resource limits                               |

### Redis Configuration Settings (`redis_conf`)

Default Redis configuration:

```yaml
redis_conf:
  port: "{{ redis_port }}"
  bind: "0.0.0.0"
  requirepass: "{{ redis_password }}"
```

## Dependencies

- [community.docker](https://docs.ansible.com/ansible/latest/collections/community/docker/index.html) collection

## Example Playbook

```yaml
- hosts: redis_servers
  vars:
    redis_version: "7.0.11"
    redis_password: "securepassword"
    redis_networks:
      - name: "app_network"
    redis_conf:
      port: "6379"
      bind: "0.0.0.0"
      maxmemory: "256mb"
      maxmemory-policy: "allkeys-lru"
    redis_cpu_requests: 0.1
    redis_cpu_limits: 0.5
    redis_memory_requests: "32M"
    redis_memory_limits: "1G"
  roles:
    - brpaz.swarm_redis
```

## Extending Redis Configuration

The `redis_conf` dictionary allows for setting any Redis configuration directives. To add configuration while keeping defaults, you can use the `combine` filter:

```yaml
- hosts: redis_servers
  vars:
    custom_redis_conf:
      maxmemory: "2gb"
      maxmemory-policy: "allkeys-lru"
    redis_conf: "{{ lookup('ansible.builtin.vars', 'redis_conf') | default({}) | combine(custom_redis_conf) }}"
  roles:
    - brpaz.swarm_redis
```

## Contributing

Check [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 🫶 Support

If you find this project helpful and would like to support its development, there are a few ways you can contribute:

[![Sponsor me on GitHub](https://img.shields.io/badge/Sponsor-%E2%9D%A4-%23db61a2.svg?&logo=github&logoColor=red&&style=for-the-badge&labelColor=white)](https://github.com/sponsors/brpaz)

<a href="https://www.buymeacoffee.com/Z1Bu6asGV" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

## 📃 License

Distributed under the MIT License.
See [LICENSE](LICENSE.md) file for details.

## 📩 Contact

✉️ **Email** - [oss@brunopaz.dev](oss@brunopaz.dev)

🖇️ **Source code**: [https://github.com/brpaz/ansible-role-swarm](https://github.com/brpaz/ansible-role-swarm)


