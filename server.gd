extends Node  # السيرفر لا يحتاج 2D أو 3D لأنه لا يعرض رسومات

var peer = ENetMultiplayerPeer.new()  # نظام الشبكة
var rooms = {}  # قائمة الغرف المفتوحة
var max_players_per_room = 6  # الحد الأقصى لكل غرفة

func _ready():
	start_server()

func start_server():
	var error = peer.create_server(12345, 100)
	if error != OK:
		print("❌ فشل تشغيل السيرفر!")
		return
	multiplayer.multiplayer_peer = peer
	multiplayer.peer_connected.connect(_on_player_connected)
	multiplayer.peer_disconnected.connect(_on_player_disconnected)
	print("✅ السيرفر يعمل على المنفذ 12345")

func _on_player_connected(id):
	print("🔗 لاعب متصل: ", id)
	assign_player_to_room(id)

func _on_player_disconnected(id):
	print("🔴 لاعب خرج: ", id)
	remove_player_from_room(id)

func assign_player_to_room(player_id):
	for room_id in rooms:
		if len(rooms[room_id]) < max_players_per_room:
			rooms[room_id].append(player_id)
			print("🎮 اللاعب", player_id, "انضم إلى الغرفة", room_id)
			check_room_status(room_id)
			return
	
	var new_room_id = rooms.size() + 1
	rooms[new_room_id] = [player_id]
	print("🆕 غرفة جديدة", new_room_id, "تم إنشاؤها")

func remove_player_from_room(player_id):
	for room_id in rooms:
		if player_id in rooms[room_id]:
			rooms[room_id].erase(player_id)
			print("🚪 اللاعب", player_id, "خرج من الغرفة", room_id)
			if rooms[room_id].is_empty():
				rooms.erase(room_id)
				print("❌ الغرفة", room_id, "تم حذفها")

func check_room_status(room_id):
	if len(rooms[room_id]) == max_players_per_room:
		print("🏁 الغرفة", room_id, "ممتلئة! بدء السباق 🚀")
		start_race(room_id)

func start_race(room_id):
	print("🏎️ السباق في الغرفة", room_id, "يبدأ الآن!")
	await get_tree().create_timer(10.0).timeout
	finish_race(room_id)

func finish_race(room_id):
	print("🏆 أول لاعب وصل إلى خط النهاية! بدء العد التنازلي...")
	for player_id in rooms[room_id]:
		rpc_id(player_id, "start_results_countdown", 5)

	await get_tree().create_timer(5.0).timeout

	print("📊 نقل اللاعبين إلى واجهة النتائج")
	for player_id in rooms[room_id]:
		rpc_id(player_id, "show_results_screen")

	await get_tree().create_timer(10.0).timeout

	print("🔄 إخراج اللاعبين الذين لم يغادروا بعد")
	for player_id in rooms[room_id]:
		rpc_id(player_id, "force_exit_to_main_menu")

	rooms.erase(room_id)
	print("🗑️ الغرفة", room_id, "تم حذفها نهائيًا بعد عرض النتائج")

@rpc("reliable")
func start_results_countdown(seconds):
	pass

@rpc("reliable")
func show_results_screen():
	pass

@rpc("reliable")
func force_exit_to_main_menu():
	pass
