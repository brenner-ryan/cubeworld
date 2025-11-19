# Life Cube Desktop Widget

A minimalist desktop widget that displays animated GIFs based on your calendar state.

## Features

- **200x200 pixel minimalist window** titled "Academic Cube"
- **State-aware animations**:
  - Shows `idle.gif` when you're free
  - Shows `stressed.gif` when you have an active event
- **Calendar integration**: Reads from `my_schedule.ics` every 30 seconds
- **Timezone-aware**: Uses UTC for accurate time comparisons
- **Error-resilient**: Defaults to IDLE state if calendar file is missing or invalid

## Requirements

- Python 3.7+
- tkinter (usually comes with Python, or install via `python3-tk` on Ubuntu/Debian)
- See `requirements.txt` for Python package dependencies

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. On Ubuntu/Debian, you may also need to install tkinter:
   ```bash
   sudo apt-get install python3-tk
   ```

## Usage

1. Update `my_schedule.ics` with your calendar events in iCalendar format
2. Run the application:
   ```bash
   python3 main.py
   ```

The widget will automatically:
- Check your schedule every 30 seconds
- Switch between idle and stressed animations based on active events
- Display the appropriate animation in the window

## Project Structure

```
.
├── main.py              # Main application code
├── my_schedule.ics      # Your calendar file (iCalendar format)
├── requirements.txt     # Python dependencies
└── assets/
    ├── idle.gif        # Animation shown when IDLE
    └── stressed.gif    # Animation shown when BUSY
```

## Customization

You can replace the GIF files in the `assets/` directory with your own animations:
- `idle.gif`: Displayed when no events are active
- `stressed.gif`: Displayed when an event is happening

Both files should be animated GIFs with dimensions of 200x200 pixels for best results.

## How It Works

1. The application parses `my_schedule.ics` using the `icalendar` library
2. It compares the current time (in UTC) with event start/end times
3. If the current time falls within any event's time range, the state is **BUSY**
4. Otherwise, the state is **IDLE**
5. The appropriate animated GIF loops in the window based on the current state
