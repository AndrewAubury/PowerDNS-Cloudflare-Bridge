# PowerDNS-Cloudflare Bridge Docker Image

This Docker image provides an integration bridge between PowerDNS and Cloudflare, allowing for dynamic updates of rDNS records managed by Cloudflare. It uses a Python Flask application to handle API requests and updates rDNS through a command-line interface.

## Docker Image

The image is available on Docker Hub and can be pulled using the following command:

```
docker pull andrewaubury/powerdns-cloudflare-bridge
```

## Prerequisites

- Docker installed on your machine.
- A Cloudflare account with API token or Key and Email.

## Configuration

Before running the container, you need to have a configuration file `CloudflareRDNS.yaml` on your host machine configured with your Cloudflare credentials. This file will be mounted into the Docker container to ensure the application can authenticate with Cloudflare API.

Here's an example structure for `CloudflareRDNS.yaml`:

```
api_token: "your_cloudflare_api_token"
email: "your_email@example.com"
key: "your_cloudflare_global_api_key"
use_token: true  # Use true to use token, false to use key and email
```

## Running the Container

To run the container with the necessary port mappings and volume mount, use the following command:

```
docker run -p 8981:8981 -v /path/to/your/CloudflareRDNS.yaml:/app/CloudflareRDNS.yaml andrewaubury/powerdns-cloudflare-bridge
```

Replace `/path/to/your/CloudflareRDNS.yaml` with the actual path to your configuration file. This command does the following:

- Maps port 8981 of the container to port 8981 on the host, allowing external access to the API.
- Mounts the `CloudflareRDNS.yaml` configuration file from the host to the container to ensure it can authenticate with the Cloudflare API.

## API Usage

The Docker container runs a Flask server that exposes endpoints to manage DNS zones:

- **GET `/api/v1/servers/localhost/zones`**: Fetches all zones.
- **POST `/api/v1/servers/localhost/zones`**: Adds a new zone.
- **GET `/api/v1/servers/localhost/zones/<zone>`**: Retrieves details of a specific zone.
- **PATCH `/api/v1/servers/localhost/zones/<zone>`**: Updates PTR records for a specific zone.

Example of updating a PTR record:

```
curl -X PATCH http://localhost:8981/api/v1/servers/localhost/zones/1.2.3.4.in-addr.arpa -d '{"rrsets": [{"name": "4.3.2.1.in-addr.arpa.", "type": "PTR", "records": [{"content": "example.com"}]}]}'
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on the GitHub repository associated with this Docker image.

## Support

For support, please open an issue in the Docker image's GitHub repository.

