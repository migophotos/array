class Item:
    def __init__(self, key=None, value=None, next_item=None, prev_item=None):
        self.value = value
        self.key = key
        self.prev = prev_item
        self.next = next_item

    def get(self):
        return [self.value, self.key]


class Array:
    def __init__(self, length=0, initial_value=0):
        self.__last = None
        self.__items = None
        if length:
            self.__add(initial_value, count=length)

    def __add(self, val, key=None, count=1):
        prev_item = None if not self.__last else self.__last

        for index in range(0, count):
            item = Item(value=val, key=key, prev_item=prev_item)

            if not self.__items:
                self.__items = item
                prev_item = item
                self.__last = item
            else:
                prev_item.next = item
                prev_item = item
                self.__last = prev_item

    def __at(self, index=None, key=None, value=None) -> Item:
        item = self.__items
        count = 0
        while item:
            if index and index == count:
                return item
            if key and key == item.key:
                return item
            if value and value == item.value:
                return item
            item = item.next
            count += 1

        return None

    def length(self):
        item = self.__items
        length = 0
        while item:
            length += 1
            item = item.next
        return length

    def set(self, index, value=None, key=None):
        item: Item = self.__at(index=index)
        if item:
            item.key = key if key else item.key
            item.value = value if value else item.value
            return True
        return False

    def insert(self, value, key=None, at_index=0):
        item = self.__items
        index = 0
        while item:
            if at_index == index:
                break
            item = item.next
            index += 1

        if not item:
            return False    # out of index

        new_item = Item(value=value, key=key)
        if at_index == 0:
            new_item.next = self.__items
            self.__items = new_item
            new_item.next.prev = self.__items
        else:
            new_item.next = item
            new_item.prev = item.prev
            new_item.prev.next = new_item
            item.prev = new_item

        return True

    def delete(self, at_index=None, value=None, key=None):
        item = self.__items

        index = 0
        while item:
            if at_index and at_index == index:
                break
            if value and value == item.value:
                break
            if key and key == item.key:
                break

            item = item.next
            index += 1
        if not item:
            return False

        if index == 0:
            to_be_deleted = self.__items
            self.__items = to_be_deleted.next
            del to_be_deleted
        else:
            to_be_deleted = item
            item.prev.next = item.next
            if item.next:
                item.next.prev = item.prev
            del to_be_deleted

        return True

    def __str__(self):
        result = "["
        item = self.__items
        while item:
            key_str = val_str = ""
            if type(item.key) == str:
                key_str = f"'{item.key}'"
            else:
                key_str = f"{item.key}"

            if type(item.value) == str:
                val_str = f"'{item.value}'"
            else:
                val_str = f"{item.value}"
            result += f"{key_str}: {val_str},"
            item = item.next

        result += "]"
        return result

    def index(self, val=None, key=None):
        index = -1
        item = self.__items
        while item:
            if val and val == item.value:
                index += 1
                break
            if key and key == item.key:
                index += 1
                break
            item = item.next
            index += 1

        return index

    def value(self, index=None, key=None):
        value = None
        item = self.__items
        count = 0
        while item:
            if index and index == count:
                value = item.value
                break
            if key and key == item.key:
                value = item.value
                break
            item = item.next
            count += 1

        return value

    def key(self, index=None, val=None):
        key = None
        item = self.__items
        count = 0
        while item:
            if index and index == count:
                key = item.key
                break
            if val and val == item.value:
                key = item.key
                break
            item = item.next
            count += 1

        return key

    def at(self, index=None, key=None, value=None):
        item = self.__items
        count = 0
        while item:
            if index and index == count:
                return item.get()
            if key and key == item.key:
                return item.get()
            if value and value == item.value:
                return item.get()
            item = item.next
            count += 1

        return None

    def append(self, val, key=None, count=1):
        self.__add(val=val, key=key, count=count)


if __name__ == "__main__":
    test_array = Array()
    for i in range(0, 100):
        test_array.append(i, f"k.{i}")

    print(test_array)
    print(test_array.index(val=50))
    print(test_array.index(key="k.50"))
    print(test_array.length())
    print(test_array.delete(50))
    print(test_array.length())

    if test_array.set(10, 100, key="k.100"):
        print(test_array)

