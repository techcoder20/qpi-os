#!/bin/sh
#
# ufetch-raspbian - tiny system info for raspbian

## INFO

# user is already defined
host="$(hostname)"
os='Raspbian'
kernel="$(uname -sr)"
uptime="$(uptime -p | sed 's/up //')"
packages="$(dpkg -l | wc -l)"
shell="$(basename "${SHELL}")"

## UI DETECTION

parse_rcs() {
	for f in "${@}"; do
		wm="$(tail -n 1 "${f}" 2> /dev/null | cut -d ' ' -f 2)"
		[ -n "${wm}" ] && echo "${wm}" && return
	done
}

rcwm="$(parse_rcs "${HOME}/.xinitrc" "${HOME}/.xsession")"

ui='unknown'
uitype='UI'
if [ -n "${DE}" ]; then
	ui="${DE}"
	uitype='DE'
elif [ -n "${WM}" ]; then
	ui="${WM}"
	uitype='WM'
elif [ -n "${XDG_CURRENT_DESKTOP}" ]; then
	ui="${XDG_CURRENT_DESKTOP}"
	uitype='DE'
elif [ -n "${DESKTOP_SESSION}" ]; then
	ui="${DESKTOP_SESSION}"
	uitype='DE'
elif [ -n "${rcwm}" ]; then
	ui="${rcwm}"
	uitype='WM'
elif [ -n "${XDG_SESSION_TYPE}" ]; then
	ui="${XDG_SESSION_TYPE}"
fi

ui="$(basename "${ui}")"

## DEFINE COLORS

# probably don't change these
if [ -x "$(command -v tput)" ]; then
	bold="$(tput bold)"
	black="$(tput setaf 0)"
	red="$(tput setaf 1)"
	green="$(tput setaf 2)"
	yellow="$(tput setaf 3)"
	blue="$(tput setaf 4)"
	magenta="$(tput setaf 5)"
	cyan="$(tput setaf 6)"
	white="$(tput setaf 7)"
	reset="$(tput sgr0)"
fi

# you can change these
lc="${reset}${bold}${red}"          # labels
nc="${reset}${bold}${red}"          # user and hostname
ic="${reset}"                       # info
c0="${reset}${green}"               # first color
c1="${reset}${red}"                 # second color

## OUTPUT

cat <<EOF

${c0}    __  __    ${nc}${USER}${ic}@${nc}${host}${reset}
${c0}   (_\\)(/_)   ${lc}OS:        ${ic}${os}${reset}
${c1}   (_(__)_)   ${lc}KERNEL:    ${ic}${kernel}${reset}
${c1}  (_(_)(_)_)  ${lc}UPTIME:    ${ic}${uptime}${reset}
${c1}   (_(__)_)   ${lc}PACKAGES:  ${ic}${packages}${reset}
${c1}     (__)     ${lc}SHELL:     ${ic}${shell}${reset}
${c1}              ${lc}${uitype}:        ${ic}${ui}${reset}

EOF
