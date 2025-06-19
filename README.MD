# Errika ✨ - Beautiful Translucent Todo Widget

A modern, translucent, draggable todo application for Mac and Linux that stays on your desktop until you close it.

![Errika Todo Widget](https://via.placeholder.com/400x500/2c2c2c/64b5f6?text=Errika+Todo+Widget)

## Features ✨

- **🎨 Beautiful Design**: Modern dark theme with translucent background
- **📱 Always Visible**: Stays on top of other windows but doesn't steal focus
- **🖱️ Draggable**: Click and drag to move anywhere on your screen
- **📋 Full Todo Management**: Add, edit, delete, and mark todos as complete
- **🏷️ Priority System**: Set priorities (Low, Medium, High, Urgent) with color coding
- **💾 Persistent Storage**: Automatically saves todos to `~/.config/errika/todos.json`
- **📊 Smart Sorting**: Incomplete todos first, then sorted by priority
- **🔢 Live Statistics**: Shows total, completed, and pending todo counts
- **⌨️ Keyboard Shortcuts**: Press Enter to quickly add todos
- **🖥️ Cross-Platform**: Works on both Mac and Linux

## Installation

### Prerequisites

You need Python 3.6+ with tkinter support. Most systems have this by default.

**Check if you have Python and tkinter:**
```bash
python3 --version
python3 -c "import tkinter; print('tkinter is available')"
```

### For Mac Users

```bash
# If you don't have Python or tkinter
brew install python-tk

# Or using MacPorts
sudo port install py39-tkinter
```

### For Linux Users

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S python python-tkinter
```

## Setup Instructions

### Method 1: Direct Download and Run

1. **Download the script:**
   ```bash
   curl -o errika.py https://raw.githubusercontent.com/your-repo/errika/main/errika.py
   ```

2. **Make it executable:**
   ```bash
   chmod +x errika.py
   ```

3. **Run Errika:**
   ```bash
   python3 errika.py
   ```

### Method 2: Install as Command Line Tool

1. **Create the errika command:**
   ```bash
   # Copy the script to a location in your PATH
   sudo cp errika.py /usr/local/bin/errika
   sudo chmod +x /usr/local/bin/errika
   ```

2. **Now you can run it from anywhere:**
   ```bash
   errika
   ```

### Method 3: Create Desktop Application (Linux)

1. **Create a desktop entry:**
   ```bash
   cat > ~/.local/share/applications/errika.desktop << EOF
   [Desktop Entry]
   Name=Errika Todo Widget
   Comment=Beautiful translucent todo application
   Exec=/usr/local/bin/errika
   Icon=accessories-text-editor
   Type=Application
   Categories=Utility;Office;
   StartupWMClass=errika
   EOF
   ```

2. **Update desktop database:**
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

## Usage Guide

### Basic Operations

1. **Adding Todos:**
   - Type your todo in the text field
   - Select priority (Low, Medium, High, Urgent)
   - Click "Add Todo" or press Enter

2. **Managing Todos:**
   - ✅ **Complete**: Click the checkbox to mark as done
   - ✏️ **Edit**: Click the edit button (✏️) to modify text
   - 🗑️ **Delete**: Click the delete button (🗑️) to remove

3. **Window Controls:**
   - **Drag**: Click and hold anywhere on the window to move it
   - **Minimize**: Click the "−" button
   - **Close**: Click the "✕" button

### Priority System

- 🔴 **Urgent**: Red color, highest priority
- 🟠 **High**: Orange color, high priority  
- 🔵 **Medium**: Blue color, default priority
- 🟢 **Low**: Green color, lowest priority

### Data Storage

Your todos are automatically saved to:
- **Mac**: `~/.config/errika/todos.json`
- **Linux**: `~/.config/errika/todos.json`

## Keyboard Shortcuts

- **Enter**: Add new todo (when text field is focused)
- **Cmd+Q** (Mac) / **Ctrl+Q** (Linux): Quit application

## Customization

You can modify the appearance by editing these variables in the script:

```python
# Window transparency (0.0 to 1.0)
self.root.attributes('-alpha', 0.9)

# Window size
self.root.geometry("350x500")

# Colors
colors = {
    'Low': '#81c784',      # Green
    'Medium': '#64b5f6',   # Blue  
    'High': '#ffb74d',     # Orange
    'Urgent': '#e57373'    # Red
}
```

## Troubleshooting

### Common Issues

**1. "tkinter not found" error:**
```bash
# Install tkinter
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

**2. Window doesn't appear translucent:**
- This is normal on some Linux desktop environments
- The app will still work perfectly, just without transparency

**3. Can't drag the window:**
- Try dragging from the header area with the title
- Ensure you're not dragging from buttons or input fields

**4. Todos not saving:**
- Check if `~/.config/errika/` directory exists
- Ensure you have write permissions to your home directory

### Platform-Specific Notes

**macOS:**
- Transparency works best on macOS 10.14+
- You might need to grant accessibility permissions

**Linux:**
- Transparency requires a compositing window manager
- Works best with GNOME, KDE, or other modern desktop environments

## Contributing

Found a bug or want to add a feature? Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on both Mac and Linux if possible
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created with ❤️ for productivity enthusiasts who love beautiful, functional tools.

---

**Enjoy using Errika! 🚀**

*For support or feature requests, please open an issue on GitHub.*