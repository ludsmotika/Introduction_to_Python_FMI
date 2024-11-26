CONCRETE_DENSITY = 2500
BRICK_DENSITY = 2000
STONE_DENSITY = 1600
WOOD_DENSITY = 600
STEEL_DENSITY = 7700
BASE_MATERIALS_COUNT = 5
BASE_MATERIAL_DENSITIES = [BRICK_DENSITY,
                           CONCRETE_DENSITY,
                           STEEL_DENSITY,
                           STONE_DENSITY,
                           WOOD_DENSITY]

ERROR_MESSAGE = "6ff9dc6e00d1e166f1612e919e934af22eb204b931539f629e152324a2e5a221"


class Material:
    density = 0

    def __init__(self, mass):
        self.mass = mass
        self.is_used = False

    @property
    def volume(self):
        if self.density == 0:
            raise ZeroDivisionError(ERROR_MESSAGE)
        return self.mass / self.density


class Concrete(Material):

    def __init__(self, mass):
        super().__init__(mass)
        Concrete.density = CONCRETE_DENSITY


class Brick(Material):

    def __init__(self, mass):
        super().__init__(mass)
        Brick.density = BRICK_DENSITY


class Stone(Material):

    def __init__(self, mass):
        super().__init__(mass)
        Stone.density = STONE_DENSITY


class Wood(Material):

    def __init__(self, mass):
        super().__init__(mass)
        Wood.density = WOOD_DENSITY


class Steel(Material):

    def __init__(self, mass):
        super().__init__(mass)
        Steel.density = STEEL_DENSITY


BASE_MATERIAL_CLASSES = [Brick, Concrete, Steel, Stone, Wood]
BASE_MATERIALS_NAMES = [x.__name__ for x in BASE_MATERIAL_CLASSES]


class Factory:
    alloys = [*BASE_MATERIAL_CLASSES]
    created_materials_from_factories = []

    def __init__(self):
        self.created_materials = []

    def __call__(self, *args, **kwargs):
        if (args and kwargs) or (not args and not kwargs):
            raise ValueError(ERROR_MESSAGE)

        return self._kwargs_case_handler(**kwargs) if kwargs else self._args_case_handler(*args)

    def _kwargs_case_handler(self, **kwargs):
        result = []
        for class_name, mass in kwargs.items():
            class_type = next((cls for cls in self.alloys if cls.__name__ == class_name), None)

            if class_type is None:
                raise ValueError(ERROR_MESSAGE)

            current_created_material = class_type(mass)
            self.created_materials.append(current_created_material)
            self.created_materials_from_factories.append(current_created_material)
            result.append(current_created_material)

        return tuple(result)

    def _args_case_handler(self, *args):
        concatenated_names = "_".join([arg.__class__.__name__ for arg in args])
        extracted_base_names = set(concatenated_names.split("_"))
        current_class_name = '_'.join(sorted(extracted_base_names))

        if any([arg.is_used for arg in args]):
            raise AssertionError(ERROR_MESSAGE)

        if current_class_name not in [current_class.__name__ for current_class in self.alloys]:
            current_class_density = sum(
                [BASE_MATERIAL_DENSITIES[i]
                 for i in range(BASE_MATERIALS_COUNT)
                 if BASE_MATERIALS_NAMES[i] in extracted_base_names]
            )
            current_class_density /= len(extracted_base_names)

            self.alloys.append(type(current_class_name, (Material,), {"density": current_class_density}))

        for arg in args:
            arg.is_used = True

        current_instance_mass = sum([arg.mass for arg in args])
        current_class_type = next(cls for cls in self.alloys if cls.__name__ == current_class_name)
        current_created_material = current_class_type(current_instance_mass)
        self.created_materials.append(current_created_material)
        self.created_materials_from_factories.append(current_created_material)
        return current_created_material

    def can_build(self, wall_volume):
        materials_volume = sum(mat.volume for mat in self.created_materials if not mat.is_used)
        return materials_volume >= wall_volume

    @classmethod
    def can_build_together(cls, wall_volume):
        materials_volume = sum(mat.volume for mat in cls.created_materials_from_factories if not mat.is_used)
        return materials_volume >= wall_volume
