# PictureDateRectifier

## Overview

**PictureDateRectifier** is a Python-based terminal application designed for Windows machines. This tool helps users correct incorrect creation timestamps of image files by extracting accurate information from the EXIF data or the filename. The application is user-configurable, allowing you to choose your preferred method for timestamp correction.

## Features

- **EXIF Data Extraction**: Automatically reads the correct creation date from the EXIF metadata of image files.
- **Filename Parsing**: Optionally, you can configure the application to derive the creation date from the filename.
- **User-Friendly Terminal Interface**: Simple command-line interface for easy interaction.
- **Batch Processing**: Correct timestamps for multiple images in one go.
- **Binary Release**: Downloadable executable for users who prefer not to run the Python script directly.

## Requirements

- Windows Operating System
- (Optional) Python 3.x if you choose to run the script directly
- Required Python packages (if running the script)

## Installation

### Option 1: Using the Binary Release

1. Go to the [Releases](https://github.com/yourusername/PictureDateRectifier/releases) page.
2. Download the latest binary release (e.g., `PictureDateRectifier.exe`).
3. Place the executable in a directory of your choice.

### Option 2: Running from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PictureDateRectifier.git
   ```
2. Navigate to the project directory:
   ```bash
   cd PictureDateRectifier
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using the Binary Release

1. Open your terminal (Command Prompt or PowerShell).
2. Navigate to the directory where the `PictureDateRectifier.exe` is located.
3. Run the application with the following command:
   ```bash
   PictureDateRectifier.exe
   ```
4. Follow the on-screen instructions to select the method of timestamp correction (EXIF data or filename) and specify the images you want to process.

   # Configuration Overview for PictureDateRectifier

The **PictureDateRectifier** application allows users to configure various parameters when running the program. Below is an overview of the command-line arguments available for customization:

| Argument                | Type     | Required | Default     | Description                                                                                     |
|------------------------|----------|----------|-------------|-------------------------------------------------------------------------------------------------|
| `folder`               | `str`    | Yes      | N/A         | Path to the folder containing the images to be processed.                                      |
| `-e`, `--exif-test`    | `flag`   | No       | `False`     | Test if the images contain the EXIF data needed for the program to work.                       |
| `-ow`, `--overwrite`    | `flag`   | No       | `False`     | Overwrite the original files with the corrected timestamps.                                    |
| `-o`, `--output`        | `str`    | No       | N/A         | Path to the folder where the images will be saved. This is skipped when `overwrite` is set.   |
| `-p`, `--progress`      | `flag`   | No       | `False`     | Show a progress bar during the processing of images.                                          |
| `-s`, `--source`        | `str`    | No       | `filename`  | Specify the source from which to draw the date information: either `exif` or `filename`.      |
| `-d`, `--date`          | `str`    | No       | `modification` | Choose which date to set the image to: `modification`, `creation`, or `access`.               |

## Usage Example

Here’s an example of how to use these parameters when running the application:

```bash
python PictureDateRectifier.py "C:\path\to\images" -ow -o "C:\path\to\output" -p -s "exif" -d "creation"
```

In this example:
- The application will process images in the specified folder.
- It will overwrite the original files with the corrected timestamps.
- The corrected images will be saved in the specified output folder.
- A progress bar will be displayed.
- The date information will be drawn from the EXIF data.
- The creation date will be set for the images.

Feel free to adjust the parameters according to your needs!

### Running from Source

1. Open your terminal (Command Prompt or PowerShell).
2. Navigate to the directory where the `main.py` script is located.
3. Run the application with the following command:
   ```bash
   python main.py
   ```
4. Follow the on-screen instructions to select the method of timestamp correction (EXIF data or filename) and specify the images you want to process.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.
