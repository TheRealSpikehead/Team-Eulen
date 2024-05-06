CREATE TABLE address (
	id INTEGER NOT NULL, 
	street VARCHAR NOT NULL, 
	zip VARCHAR NOT NULL, 
	city VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	"_Role__access_level" INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE login (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	FOREIGN KEY(role_id) REFERENCES role (id)
);
CREATE TABLE guest (
	id INTEGER NOT NULL, 
	firstname VARCHAR NOT NULL, 
	lastname VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	address_id INTEGER NOT NULL, 
	type VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(address_id) REFERENCES address (id)
);
CREATE TABLE registred_guest (
	id INTEGER NOT NULL, 
	login_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id) REFERENCES guest (id), 
	FOREIGN KEY(login_id) REFERENCES login (id)
);
CREATE TABLE hotel (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	stars INTEGER NOT NULL, 
	address_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(address_id) REFERENCES address (id)
);
CREATE TABLE room_type (
	id INTEGER NOT NULL, 
	description VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (description)
);
CREATE TABLE amenity (
	id INTEGER NOT NULL, 
	description VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (description)
);
CREATE TABLE room_amenity (
	room_hotel_id INTEGER NOT NULL, 
	room_number VARCHAR NOT NULL, 
	"_RoomAmenity__amenity_id" INTEGER NOT NULL, 
	PRIMARY KEY (room_hotel_id, room_number, "_RoomAmenity__amenity_id"), 
	FOREIGN KEY(room_hotel_id, room_number) REFERENCES room (hotel_id, number), 
	FOREIGN KEY("_RoomAmenity__amenity_id") REFERENCES amenity (id)
);
CREATE TABLE room (
	hotel_id INTEGER NOT NULL, 
	number VARCHAR NOT NULL, 
	type_id INTEGER NOT NULL, 
	max_guests INTEGER NOT NULL, 
	description VARCHAR NOT NULL, 
	price FLOAT NOT NULL, 
	PRIMARY KEY (hotel_id, number), 
	FOREIGN KEY(hotel_id) REFERENCES hotel (id), 
	FOREIGN KEY(type_id) REFERENCES room_type (id)
);
CREATE TABLE booking (
	id INTEGER NOT NULL, 
	room_hotel_id INTEGER NOT NULL, 
	room_number VARCHAR NOT NULL, 
	guest_id INTEGER NOT NULL, 
	number_of_guests INTEGER NOT NULL, 
	start_date DATE NOT NULL, 
	end_date DATE NOT NULL, 
	comment VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(room_hotel_id, room_number) REFERENCES room (hotel_id, number), 
	FOREIGN KEY(guest_id) REFERENCES guest (id)
);
