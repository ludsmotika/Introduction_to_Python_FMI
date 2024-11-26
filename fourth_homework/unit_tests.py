import unittest
from fourth_homework import *

class BaseMaterialsTests(unittest.TestCase):
    """
    in these tests expected_density is mass and all check if expected_density/mass == 1.0
    also they test decimal places for volume
    """

    def setUp(self) -> None:
        self.factory = Factory()

    def test_density_for_concrete(self):
        expected_density = 2500
        concrete, = self.factory(Concrete=expected_density)
        self.assertEqual(concrete.volume, 1.0)

    def test_density_for_brick(self):
        expected_density = 2000
        brick, = self.factory(Brick=expected_density)
        self.assertEqual(brick.volume, 1.0)

    def test_density_for_stone(self):
        expected_density = 1600
        stone, = self.factory(Stone=expected_density)
        self.assertEqual(stone.volume, 1.0)

    def test_density_for_wood(self):
        expected_density = 600
        wood, = self.factory(Wood=expected_density)
        self.assertEqual(wood.volume, 1.0)

    def test_density_for_steel(self):
        expected_density = 7700
        steel, = self.factory(Steel=expected_density)
        self.assertEqual(steel.volume, 1.0)

    def test_for_volume_decimal_places_if_one_decimal_places(self):
        expected_density = 7700 * 7
        steel, = self.factory(Steel=expected_density)
        self.assertEqual(steel.volume, 7.0)
        self.assertIsInstance(steel.volume, float)

    def test_for_volume_decimal_places_if_more_than_places_up(self):
        # от задачата разбирам че просто трябва резултата да се форматира до 2рия знак
        # ако не е така да ме поправи някой :)
        # 4453/7700 = 0.5783116883116883 =&gt; 0.58
        expected_density = 4453
        steel, = self.factory(Steel=expected_density)
        self.assertEqual(steel.volume, 0.5783116883116883)
        self.assertIsInstance(steel.volume, float)

    def test_for_volume_decimal_places_if_more_than_places_down(self):
        # 4453/600 = 7.421666666666667 =&gt; 7.42
        expected_density = 4453
        steel, = self.factory(Wood=expected_density)
        self.assertAlmostEqual(steel.volume, 7.42, places=2)
        self.assertIsInstance(steel.volume, float)


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.factory1 = Factory()
        self.factory2 = Factory()

        self.wood1, self.steel1, self.brick1, self.stone1, self.concrete1 = self.factory1(Wood=5, Steel=15, Brick=60,
                                                                                          Stone=300, Concrete=20)
        self.wood2, self.steel2, self.brick2, self.stone2, self.concrete2 = self.factory2(Wood=5, Steel=30, Brick=300,
                                                                                          Stone=600, Concrete=2000)

    def test_factory_invalid_call_with_empy_call(self):
        with self.assertRaises(ValueError):
            self.factory1()

    def test_factory_invalid_call_with_args_and_kwargs(self):
        with self.assertRaises(ValueError):
            self.factory1(self.wood1, Wood=5)

    def test_factory_return_type(self):
        self.assertIsInstance(self.factory2(Wood=66), tuple)

    def test_two_factories_with_same_passed_arguments_produce_different_objects_of_same_type(self):
        self.assertEqual(type(self.wood1), type(self.wood2))
        self.assertEqual(self.wood1.volume, self.wood2.volume)
        self.assertNotEqual(self.wood1, self.wood2)

    def test_factory_call_with_kwargs_with_not_existing_class(self):
        with self.assertRaises(ValueError):
            self.factory1(Baba=1)

    def test_volume_for_all_instances_returned_from_factory_call_kwargs(self):
        wood, steel, stone = self.factory1(Wood=600, Steel=100, Stone=3200)
        self.assertAlmostEqual(wood.volume, 1.0, )
        self.assertAlmostEqual(steel.volume, 0.012987012987012988)
        self.assertAlmostEqual(stone.volume, 2.0)

    def test_for_recreating_already_existing_dynamic_class(self):
        wooden_steel = self.factory1(self.wood1, self.steel1)
        self.assertEqual(wooden_steel.__class__.__name__, "Steel_Wood")
        another_wooden_steel = self.factory1(self.wood2, self.steel2)
        self.assertEqual(type(wooden_steel), type(another_wooden_steel))

    def test_for_reusing_same_materials_for_creation(self):
        self.factory1(self.wood1, self.steel2)
        with self.assertRaises(AssertionError):
            self.factory1(self.wood1)

    def test_new_generated_class_name_is_sorted_in_ascending_order(self):
        result = self.factory1(self.wood1, self.steel1, self.brick1)
        self.assertEqual(result.__class__.__name__, "Brick_Steel_Wood")

        result = self.factory1(self.stone1, self.steel2, self.wood2, )
        self.assertEqual(result.__class__.__name__, "Steel_Stone_Wood")

    def test_new_generated_class_name_is_sorted_in_ascending_order2(self):
        result = self.factory1(self.wood1, self.steel2, self.stone2, self.brick1, self.concrete1)
        self.assertEqual(result.__class__.__name__, "Brick_Concrete_Steel_Stone_Wood")

    def test_volume_and_density_for_dynamically_created_materials(self):
        # density = (2500 + 7700 + 600) / 3 = 3600.
        # mass = 5 + 30 + 2000 = 2035
        # volume = 2035 / 3600 = 0.5652777777777778 = 0.57
        result = self.factory1(self.wood1, self.steel2, self.concrete2)
        self.assertAlmostEqual(result.volume, 0.5652777777777778)

    def test_different_factories_called_with_same_kwargs_return_materials_of_same_type(self):
        steel_stone = self.factory1(Stone=1, Steel=1)
        another_steel_stone = self.factory2(Steel=1, Stone=1)
        self.assertEqual(type(steel_stone), type(another_steel_stone))

    def test_one_factory_use_material_and_another_tries_to_use_it_and_fails(self):
        steel_stone = self.factory1(self.steel2, self.stone1)
        self.factory1(steel_stone)
        with self.assertRaises(AssertionError):
            self.factory2(self.wood1, steel_stone)

    def test_build_method_returns_true_for_greater_than_volume(self):
        factory = Factory()
        factory(Brick(2500))
        self.assertTrue(factory.can_build(1))

    def test_build_method_returns_true_for_equal_volume(self):
        factory = Factory()
        factory(Brick(2000))
        self.assertTrue(factory.can_build(1))

    def test_build_method_returns_false(self):
        factory = Factory()
        factory(Brick(1500))
        self.assertFalse(factory.can_build(1))

    def test_build_method_with_many_materials_returns_false(self):
        factory1 = Factory()
        brick1, wood1 = factory1(Brick=2000, Wood=1200)
        brick_wood1 = factory1(brick1, wood1)
        self.assertEqual(factory1.can_build(3), False)

    def test_build_method_with_many_materials_returns_true(self):
        # density = (2000+ 600+7700) / 3 = 3433.3333333333335
        # mass = 2000 + 1000 + 70000 = 73000
        # volume = 73000 / 3433.3333333333335 = 21.262135922330096 = 21.2
        factory1 = Factory()
        brick1, wood1, steel = factory1(Brick=2000, Wood=1000, Steel=70000)
        factory1(brick1, wood1, steel)
        self.assertTrue(factory1.can_build(21.26))
        self.assertEqual(factory1.can_build(21.27), False)

    def test_string_after_combination(self):
        result1 = self.factory1(self.wood1, self.brick1)
        result2 = self.factory2(self.concrete2, self.stone1)
        result = self.factory1(result1, result2)
        self.assertEqual(result.__class__.__name__, "Brick_Concrete_Stone_Wood")

if __name__ == "__main__":
    unittest.main()