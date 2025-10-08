import logging

# ---------- Logging-ის კონფიგურაცია ----------
logging.basicConfig(
    filename="bookings_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


# ---------- Room კლასი ----------
class Room:
    def __init__(self, room_number: int, room_type: str, price_per_night: float, max_guests: int):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = True
        self.max_guests = max_guests
        self.booked_by = None  # ახალი ველი — ვინ დააჯავშნა

    def book_room(self, customer_name: str):
        """ოთახის დაჯავშნა"""
        self.is_available = False
        self.booked_by = customer_name

    def release_room(self):
        """ოთახის გათავისუფლება"""
        self.is_available = True
        self.booked_by = None

    def calculate_price(self, nights: int) -> float:
        """ღამეების რაოდენობის მიხედვით ფასის გამოთვლა"""
        return self.price_per_night * nights

    def __str__(self):
        status = "თავისუფალია" if self.is_available else f"დაჯავშნილია ({self.booked_by})"
        return f"ოთახი №{self.room_number} | ტიპი: {self.room_type} | ფასი/ღამე: {self.price_per_night} ₾ | {status}"


# ---------- Customer კლასი ----------
class Customer:
    def __init__(self, name: str, budget: float):
        self.name = name
        self.budget = budget
        self.booked_rooms = []

    def add_room(self, room: Room):
        """ოთახის დამატება მომხმარებლის დაჯავშნაში"""
        self.booked_rooms.append(room)

    def remove_room(self, room: Room):
        """ოთახის წაშლა"""
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)

    def pay_for_booking(self, total_price: float) -> bool:
        """გადახდა და ბიუჯეტის შემოწმება"""
        if self.budget >= total_price:
            self.budget -= total_price
            return True
        else:
            print("ბიუჯეტი არასაკმარისია გადახდისთვის!")
            return False

    def show_booking_summary(self):
        """დაჯავშნის დეტალების ჩვენება"""
        if not self.booked_rooms:
            print("თქვენ არ გაქვთ დაჯავშნილი ოთახები.")
            return
        print(f"\nდაჯავშნილი ოთახები მომხმარებლისთვის: {self.name}")
        for room in self.booked_rooms:
            print(f" - {room}")
        print(f"დარჩენილი ბიუჯეტი: {self.budget:.2f} ₾\n")


# ---------- Hotel კლასი ----------
class Hotel:
    def __init__(self, name: str, rooms: list):
        self.name = name
        self.rooms = rooms
        self.bookings_log = []

    def show_available_rooms(self, room_type: str = None):
        """თავისუფალი ოთახების სია"""
        available = [room for room in self.rooms if room.is_available]
        if room_type:
            available = [room for room in available if room.room_type.lower() == room_type.lower()]
        return available

    def calculate_total_booking(self, room_number: int, nights: int) -> float:
        """ჯამური ღირებულება"""
        for room in self.rooms:
            if room.room_number == room_number:
                return room.calculate_price(nights)
        raise ValueError("ასეთი ნომრის ოთახი ვერ მოიძებნა!")

    def log_booking(self, customer: Customer, room: Room, total_price: float):
        """დაჯავშნის ლოგირება"""
        message = f"{customer.name} დაჯავშნა ოთახი №{room.room_number}, ფასი: {total_price:.2f} ₾"
        logging.info(message)
        self.bookings_log.append(message)

    def book_room_for_customer(self, customer: Customer, room_number: int, nights: int) -> bool:
        """ოთახის დაჯავშნა"""
        room = next((r for r in self.rooms if r.room_number == room_number), None)
        if room is None:
            print("ასეთი ოთახის ნომერი არ არსებობს.")
            return False
        if not room.is_available:
            print(f"ოთახი №{room.room_number} უკვე დაჯავშნილია ({room.booked_by}) მიერ.")
            return False

        total_price = self.calculate_total_booking(room_number, nights)
        print(f"ჯამური ფასი: {total_price:.2f} ₾")

        if customer.pay_for_booking(total_price):
            room.book_room(customer.name)
            customer.add_room(room)
            self.log_booking(customer, room, total_price)
            print("დაჯავშნა წარმატებით განხორციელდა!")
            return True
        return False

    def cancel_booking(self, customer: Customer, room_number: int):
        """დაჯავშნის გაუქმება"""
        for room in customer.booked_rooms:
            if room.room_number == room_number:
                room.release_room()
                customer.remove_room(room)
                print(f"დაჯავშნა ოთახზე №{room_number} გაუქმდა.")
                return
        print("მომხმარებელს ამ ნომრით დაჯავშნა არ გააჩნია.")


# ---------- მთავარი ლოგიკა ----------
def main():
    otaxebi = [
        Room(101, "Single", 100, 1),
        Room(102, "Single", 120, 1),
        Room(201, "Double", 200, 2),
        Room(202, "Double", 220, 2),
    ]
    hotel = Hotel("Grand Hotel", otaxebi)

    print("კეთილი იყოს თქვენი მობრძანება სასტუმრო 'Grand LEVAN Hotel'-ში!\n")

    while True:
        saxeli = input("შეიყვანეთ თქვენი სახელი: ").strip()
        if saxeli:
            break
        print("გთხოვთ მიუთითოთ სახელი!")

    while True:
        try:
            biujeti = float(input("შეიყვანეთ თქვენი ბიუჯეტი (₾): "))
            if biujeti > 0:
                break
            print("ბიუჯეტი უნდა იყოს დადებითი რიცხვი!")
        except ValueError:
            print("გთხოვთ შეიყვანოთ რიცხვითი მნიშვნელობა!")

    momxmarebeli = Customer(saxeli, biujeti)

    while True:
        print("\n--- მოქმედებები ---")
        print("1. თავისუფალი ოთახების ნახვა")
        print("2. ოთახის დაჯავშნა")
        print("3. დაჯავშნის გაუქმება")
        print("4. ჩემი დაჯავშნები")
        print("5. გასვლა")

        archevani = input("აირჩიეთ მოქმედება: ").strip()

        if archevani == "1":
            tipi = input("ოთახის ტიპი (Single/Double ან ყველა): ").strip()
            if tipi == "ყველა":
                rooms = hotel.rooms  # აჩვენებს ყველა ოთახს
            else:
                rooms = [r for r in hotel.rooms if r.room_type.lower() == tipi.lower()]

            if not rooms:
                print("ასეთი ტიპის ოთახები ვერ მოიძებნა.")
            else:
                print("\n ოთახების სია:")
                for r in rooms:
                    print(r)

        elif archevani == "2":
            try:
                room_number = int(input("მიუთითეთ ოთახის ნომერი: "))
                nights = int(input("ღამეების რაოდენობა: "))
                if nights <= 0:
                    print("ღამეების რაოდენობა უნდა იყოს დადებითი!")
                    continue
                hotel.book_room_for_customer(momxmarebeli, room_number, nights)
            except ValueError:
                print("გთხოვთ შეიყვანოთ რიცხვითი მნიშვნელობები!")

        elif archevani == "3":
            try:
                room_number = int(input("მიუთითეთ გასაუქმებელი ოთახის ნომერი: "))
                hotel.cancel_booking(momxmarebeli, room_number)
            except ValueError:
                print("თახის ნომერი უნდა იყოს რიცხვი!")

        elif archevani == "4":
            momxmarebeli.show_booking_summary()

        elif archevani == "5":
            print("მადლობა გამოყენებისთვის!")
            break

        else:
            print("არასწორი არჩევანი, სცადეთ თავიდან.")


if __name__ == "__main__":
    main()
