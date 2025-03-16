FROM godotengine/godot:4.0.0-stable

WORKDIR /app
COPY . .

RUN chmod +x server.gd

CMD godot4 --headless --script server.gd
