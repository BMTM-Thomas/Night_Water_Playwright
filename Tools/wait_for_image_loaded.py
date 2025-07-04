# Wait for image Appear
image_vault = None
while image_vault is None:
    image_vault = pyautogui.locateOnScreen('./image/vault.png', grayscale = True)
print("Lastpass Image Vault Loaded")