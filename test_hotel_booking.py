import unittest
from hotel_booking import Room, Customer, Hotel


class TestHotelBooking(unittest.TestCase):

    def setUp(self):
        """ტესტისთვის საწყისი ობიექტების შექმნა"""
        self.room1 = Room(101, "Single", 100, 1)
        self.room2 = Room(201, "Double", 200, 2)
        self.customer = Customer("Levan", 500)
        self.hotel = Hotel("Test Hotel", [self.room1, self.room2])

    def test_room_booking_and_release(self):
        """ტესტი: ოთახის დაჯავშნა და გათავისუფლება"""
        self.room1.book_room()
        self.assertFalse(self.room1.is_available)
        self.room1.release_room()
        self.assertTrue(self.room1.is_available)

    def test_calculate_price(self):
        """ტესტი: ფასის გამოთვლა ღამეების მიხედვით"""
        self.assertEqual(self.room1.calculate_price(3), 300)

    def test_customer_payment_success(self):
        """ტესტი: გადახდა წარმატებით"""
        result = self.customer.pay_for_booking(200)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 300)

    def test_customer_payment_fail(self):
        """ტესტი: გადახდა ბიუჯეტის უკმარისობისას"""
        result = self.customer.pay_for_booking(1000)
        self.assertFalse(result)
        self.assertEqual(self.customer.budget, 500)

    def test_hotel_booking_success(self):
        """ტესტი: დაჯავშნა წარმატებით"""
        result = self.hotel.book_room_for_customer(self.customer, 101, 2)
        self.assertTrue(result)
        self.assertFalse(self.room1.is_available)
        self.assertIn(self.room1, self.customer.booked_rooms)

    def test_hotel_booking_fail(self):
        """ტესტი: დაჯავშნა ვერ ხერხდება (არასწორი ნომერი)"""
        result = self.hotel.book_room_for_customer(self.customer, 999, 2)
        self.assertFalse(result)

    def test_cancel_booking(self):
        """ტესტი: ჯავშნის გაუქმება"""
        self.hotel.book_room_for_customer(self.customer, 101, 1)
        result = self.hotel.cancel_booking(self.customer, 101)
        self.assertTrue(result)
        self.assertTrue(self.room1.is_available)
        self.assertNotIn(self.room1, self.customer.booked_rooms)


if __name__ == "__main__":
    unittest.main()
