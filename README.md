# CryptPad Prometheus Exporter

This is a simple Prometheus exporter for CryptPad. Currently it only exports the number of registered users, but it is still a work in progress.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source venv/bin/activate
python exporter.py
```

## Configuration

Currently, the exporter can only be configured by modifying the source code. The following variables can be changed:

- `PINS_DIR`: The directory where the CryptPad pins are stored. Default: `/srv/cryptpad/data/pins`
- `PORT`: The port the exporter listens on. Default: `8000`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
