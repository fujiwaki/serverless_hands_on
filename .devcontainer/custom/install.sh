# install rye
su vscode << EOF
curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
echo 'source "/home/vscode/.rye/env"' >> ~/.zprofile
/home/vscode/.rye/shims/rye config --set-bool behavior.use-uv=true
EOF

# install CDK
su vscode << EOF
npm install -g aws-cdk
EOF
