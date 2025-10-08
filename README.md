# hotel
hotel (finaluri)

„სასტუმროს დაჯავშნის სააგენტო“ Back-End (Python)

დასახული მიზანი:
თქვენ უნდა შექმნათ მრავალფუნქციური სასტუმროს დაჯავშნის სისტემა, რომელიც აერთიანებს:  სასტუმროს ოთახების მართვას
 მომხმარებლის დაჯავშნას და გადახდას
 ფასების დინამიურ გამოთვლას სეზონის მიხედვით
 მომხმარებლის ანგარიშის მართვას
 დაჯავშნების ლოგირებას
 unittest/pytest ტესტირებას

კლასები, ატრიბუტები და მეთოდები:
კლასი Room
აღწერა: თითო ოთახი სასტუმროში
Attributes (ატრიბუტები):  room_number: int – ოთახის ნომერი
 room_type: str – ტიპი (Single, Double)  price_per_night: float – ღამეების ფასი
 is_available: bool – თავისუფალია თუ არა  max_guests: int – მაქსიმალური ადამიანების რაოდენობა
Methods (მეთოდები):  book_room(self) – დაჯავშნისას ფლაგი is_available=False
 release_room(self) – გათავისუფლებისას is_available=True
 calculate_price(self, nights: int) -> float – ფასი გათვალისწინებით ღამეების 
რაოდენობისა
 __str__(self) – ოთახის დეტალების სტრინგის სახით დაბრუნება
კლასი Customer
აღწერა: მომხმარებელი, რომელიც დაჯავშნებს აკეთებს
Attributes:  name: str – მომხმარებლის სახელი
 budget: float – ბიუჯეტი
 booked_rooms: list – დაჯავშნილი ოთახების სია
Methods:  add_room(self, room: Room) – ოთახის დამატება დაჯავშნაში
 remove_room(self, room: Room) – ოთახის წაშლა დაჯავშნიდან
 pay_for_booking(self, total_price: float) -> bool – გადახდა და ბიუჯეტის 
შემოწმება  show_booking_summary(self) – სტრინგში დაჯავშნილი ოთახები, 
ღირებულება

კლასი Hotel
აღწერა: სასტუმროს მართვის კლასი
Attributes:  name: str – სასტუმროს სახელი
 rooms: list – სასტუმროს ყველა ოთახი (Room ობიექტები)  bookings_log: list – დაჯავშნების ისტორია
Methods:  show_available_rooms(self, room_type: str = None) -> list – თავისუფალი 
ოთახების სია  book_room_for_customer(self, customer: Customer, room_number: int, nights: 
int) -> bool – კონკრეტული ოთახის დაჯავშნა მომხმარებლისთვის
 calculate_total_booking(self, room_number: int, nights: int) -> float – ჯამური 
ღირებულება  log_booking(self, customer: Customer, room: Room, total_price: float) – 
ლოგირება (შესაძლებელია logging მოდულით)  cancel_booking(self, customer: Customer, room_number: int) – დაჯავშნის 
გაუქმება

ფუნქციონალი
1. მომხმარებელი სვამს მოთხოვნებს: ოთახის ტიპი, დღეების რაოდენობა
2. სისტემა აჩვენებს თავისუფალ ოთახებს
3. მომხმარებელი ირჩევს ოთახს
4. სისტემა ამოწმებს ბიუჯეტს და საშუალებას აძლევს გადახდას
5. დაჯავშნა ნებადართულია თუ ბიუჯეტი საკმარისია
6. სისტემა განახორციელებს ქულების დაგროვებას
7. დაჯავშნა ემატება bookings_log-ში (logging + ფაილში შენახვა)
8. შესაძლებელია დაჯავშნის გაუქმება

   
ტესტირება (unittest/pytest)
Customer.pay_for_booking() – ბიუჯეტის სწორად შემცირება
Hotel.book_room_for_customer() – დაჯავშნა მხოლოდ თავისუფალ ოთახებზე
