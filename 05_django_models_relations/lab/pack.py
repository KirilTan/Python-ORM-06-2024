import os
import zipfile
import datetime


def pack():
    """
    This function creates a zip archive of specific files and directories.
    It removes any old archive before creating a new one.

    Parameters:
    None

    Returns:
    None
    """

    # Remove old archive
    for item in os.listdir('.'):
        if item.endswith(".zip"):
            os.remove(item)

    # Get current date and time for archive name
    dt = datetime.datetime.now().strftime('%H-%M_%d.%m.%y')

    # Create a new zip archive with the current date and time
    with zipfile.ZipFile(f'submission-{dt}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all files and directories in the current working directory
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, os.getcwd())
                current_dir = os.path.basename(root)

                # Add specific files and directories to the archive
                if file in ['requirements.txt', 'manage.py', 'caller.py'] \
                        or current_dir in ['main_app', 'orm_skeleton', 'migrations']:
                    zipf.write(file_path, archive_path)

    print('Submission created!')


if __name__ == '__main__':
    pack()