default:
	sudo systemctl disable --now ip.service || true
	sudo cp ip.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable --now ip.service