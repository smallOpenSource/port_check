# Port Status Checker

A simple Python script to periodically check the status of specified server ports and send notifications when a status change is detected. It is designed to be lightweight and easily automated using cron.

## Features

-   Checks a list of hosts and ports defined in a configuration file.
-   Sends notifications only when the port status changes (e.g., from UP to DOWN or DOWN to UP).
-   Prevents duplicate notifications by storing the last known status of each port.
-   Easy to configure via a simple text file (`port_check.lst`).
-   Can be easily automated with a scheduler like cron.

## Requirements

-   Python 3.x
-   A notification script (`push_msg.py`) that can accept a message as a command-line argument.

## Setup

1.  **Clone or download the repository.**

2.  **Configure the port list:**
    Create or edit the `port_check.lst` file. Add the services you want to monitor, with one entry per line. The format is:
    ```
    [Host] [Port] [Description (Optional)]
    ```
    -   `Host`: The hostname or IP address to check.
    -   `Port`: The port number.
    -   `Description`: An optional friendly name for the service.

    **Example `port_check.lst`:**
    ```
    # Host          Port  Description
    google.com      443   Google Search
    1.1.1.1         53    Cloudflare DNS
    ```

3.  **Implement your notification logic:**
    The `port_checker.py` script calls `push_msg.py` to send notifications. You must implement your own notification mechanism inside `push_msg.py`. This could be sending a message to Slack, Telegram, a custom API, or sending an email.

    The script will be called with the notification message as a single argument.
    -   **On Failure:** `"My Web Server (1.2.3.4:80) 장애 (2025.07.05 15:30:00)"`
    -   **On Recovery:** `"My Web Server (1.2.3.4:80) 복구 (2025.07.05 15:35:00)"`

## Usage

### Manual Execution

You can run the script manually from the command line to test its operation.

```bash
/path/to/your/python /app/mng/port_checker.py
```
*Replace `/path/to/your/python` with the actual path to your Python interpreter (e.g., `/usr/bin/python3`).*

### Automation with Cron

To run the check automatically every 5 minutes, add the following line to your crontab.

1.  Open the crontab editor:
    ```bash
    crontab -e
    ```

2.  Add the following line, making sure to use the absolute path to your Python interpreter and the script:
    ```cron
    */5 * * * * /path/to/your/python /app/mng/port_checker.py
    ```

    **Example:**
    ```cron
    */5 * * * * /app/miniconda3/envs/simpleClient/bin/python /app/mng/port_checker.py
    ```

### Logging

It is recommended to redirect the script's output to a log file when running it with cron. This helps in debugging and keeping a record of events.

Modify your crontab entry as follows:

```cron
*/5 * * * * /path/to/your/python /app/mng/port_checker.py >> /app/mng/port_checker.log 2>&1
```
-   `>> /app/mng/port_checker.log`: Appends the standard output to a log file.
-   `2>&1`: Redirects standard error to the same location as the standard output, ensuring errors are also logged.

## How It Works

1.  The script reads the list of hosts and ports from `port_check.lst`.
2.  It loads the previous status of all ports from `port_check_status.json`. If the file doesn't exist, it's created.
3.  For each entry, it attempts to open a TCP connection to the specified host and port.
4.  It compares the current status (UP/DOWN) with the previous status.
5.  If the status has changed, it calls the `push_msg.py` script with a formatted notification message.
6.  Finally, it saves the current status of all ports to `port_check_status.json` for the next run.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
