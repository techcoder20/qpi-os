# Installing Qtile

# Installing Dependencies
sudo apt update
sudo apt install libxcb-render0-dev libffi-dev libcairo2 libpangocairo-1.0-0
pip3 install --user dbus-next
pip3 install --user xcffib
pip3 install --user cairocffi[xcb]
path=$(python -m site --user-site)
python3 $path/cairocffi/ffi_build.py

# Compiling Qtile
git clone git://github.com/qtile/qtile.git ~/qpi-os/qtile
cd ~/qpi-os/qtile
pip3 install .

# Backing Up Config Files
sudo mv /etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart.bak
sudo mv /etc/xdg/lxsession/LXDE-pi/desktop.conf /etc/xdg/lxsession/LXDE-pi/autostart/desktop.conf.bak

# Installing Required apps
sudo apt install nautilus nitrogen xfce4-terminal blueman

# Installing Starthship prompt
sh -c "$(curl -fsSL https://starship.rs/install.sh)"
echo 'eval "$(starship init bash)"' >> .bashrc

# Installing ufetch
cp ~/qpi-os/assets/.ufetch.sh ~/
echo '~/.ufetch.sh' >> .bashrc

# Installing picom
sudo apt install libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libconfig-dev libgl1-mesa-dev libpcre2-dev libpcre3-dev libevdev-dev uthash-dev libev-dev libx11-xcb-dev meson
git clone https://github.com/ibhagwan/picom ~/qpi-os/picom
cd ~/qpi-os/picom
meson --buildtype=release . build
ninja -C build
ninja -C build install

# Installing micro text editor
curl https://getmic.ro | bash
sudo mv micro /usr/bin
micro -plugin install nordcolors

# Installing Pi Apps
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash

# Installing Ulauncher
~/pi-apps/manage install Ulauncher

# Installing Themes And Icons And Fonts
wget -qO- https://git.io/papirus-icon-theme-install | DESTDIR="$HOME/.icons" sh

wget https://github.com/EliverLara/Nordic/releases/download/v2.1.0/Nordic-darker-standard-buttons.tar.xz
tar -xf Nordic-darker-standard-buttons.tar.xz
rm Nordic-darker-standard-buttons.tar.xz
mkdir ~/.themes
mv Nordic-darker-standard-buttons ~/.themes

mkdir ~/.fonts
cp ~/qpi-os/assets/.fonts/* ~/.fonts

# Copying all configs
cp ~/qpi-os/assets/LXDE-pi/* /etc/xdg/lxsession/LXDE-pi/
cp ~/qpi-os/assets/.config/* ~/.config
mkdir ~/.local/share/wallpapers
cp ~/qpi-os/wallpaper.png ~/.local/share/wallpapers

# Installing Network Manager
sudo apt -y install network-manager network-manager-gnome 

sudo systemctl enable network-manager &>/dev/null

sudo sed -i '/denyinterfaces wlan0/c\ ' /etc/dhcpcd.conf 
echo "denyinterfaces wlan0" | sudo tee -a /etc/dhcpcd.conf &>/dev/null

sudo sed -i '/[main]/,/managed=true/d' /etc/NetworkManager/NetworkManager.conf 
echo '''
[main]
plugins=ifupdown,keyfile
dhcp=internal
[ifupdown]
managed=true''' | sudo tee -a /etc/NetworkManager/NetworkManager.conf &>/dev/null


echo -e -n  "${RED}WARNING! It appears there is already a backup at ~/.local/share/MacOSBigSurThemeConverter/.config_backup. Do you want to overwrite ? [Y/n] ${NC}"
read -r answer
if [ "$answer" == 'n' ];then
  echo "OK, Not Going to overwrite :)"
  exit
fi

echo 'Please Restart Your Device Now'
