import testinfra


def test_redis_service_running(host):
    cmd = host.run(
        "docker service ls --filter name=redis --format '{{.Name}} {{.Replicas}}'"
    )
    assert cmd.rc == 0
    assert "redis" in cmd.stdout
    assert "1/1" in cmd.stdout


def test_redis_container_healthy(host):
    cmd = host.run("docker ps --filter name=redis --format '{{.Names}}'")
    assert cmd.rc == 0
    container_name = cmd.stdout.strip()
    assert container_name != ""

    inspect = host.run(
        f"docker inspect --format='{{{{.State.Health.Status}}}}' {container_name}"
    )

    assert inspect.stdout.strip() == "healthy"


def test_redis_responds_on_port(host):
    """Test that Redis responds to ping commands on the default port."""
    redis_port = 6379
    # Get the first Redis container ID without interactive flag which is not needed
    container_id = host.run(
        "docker ps --filter 'name=redis' -q | head -n1"
    ).stdout.strip()

    # Ensure we found a container
    assert container_id, "No Redis container found"

    # Execute the ping command in the container
    result = host.run(
        f"docker exec {container_id} redis-cli -h localhost -p {redis_port} ping"
    )

    # Check response
    assert result.rc == 0, f"Redis ping command failed with: {result.stderr}"
    assert (
        result.stdout.strip() == "PONG"
    ), f"Expected PONG, got: {result.stdout.strip()}"
