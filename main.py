from totallib import *

# Connect()
#
# account = Account()
#
# account.deposit()
# Connect()

dir_path = "C:\\연습\\연습3"
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
os.makedirs("C:\\연습\\연습4", exist_ok=True)