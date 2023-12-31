from typing import List, Dict


class Item:
    """

    """
    def __init__(self, key=None, value=None, next_item=None, prev_item=None):
        self.value = value
        self.key = key
        self.prev = prev_item
        self.next = next_item

    def get(self) -> Dict:
        if self.key is None:
            return self.value
        else:
            return {self.key: self.value}


class Array:
    """
    Array implementation with handy API
    """
    def __init__(self, length=0, initial_value=0, from_list=[], from_dict={}):
        self.__next = None
        self.__last = None
        self.__items = None
        self.__length = 0
        self.__sorted_list = []
        if length:
            self.__add(initial_value, count=length)
        if len(from_list):
            for il in from_list:
                self.__add(il)

        for dk in from_dict:
            self.__add(from_dict[dk], key=dk)

        self.__length = self.length()

    def __str__(self):
        result = "["
        item = self.__items
        key_str = val_str = ""
        while item:
            if type(item.key) == str:
                key_str = f"'{item.key}'"
            else:
                key_str = f"{item.key}"

            if type(item.value) == str:
                val_str = f"'{item.value}'"
            else:
                val_str = f"{item.value}"

            if len(result) > 1:
                result += ","

            if key_str.find("None") >= 0:
                result += f"{val_str}"
            else:
                result += f"{key_str}: {val_str}"

            item = item.next

        result += "]"
        return result

    def __iter__(self):
        return self

    def __next__(self):
        if self.__next is None:
            self.__next = self.__items

        elif self.__next.next:
            self.__next = self.__next.next

        else:
            self.__next = None
            raise StopIteration

        return self.__next.value if self.__next.key is None else {self.__next.key: self.__next.value}

    def __getitem__(self, item):
        return self.at(index=item)

    def __setitem__(self, index, value):
        if type(value) == dict:
            for k in value:
                self.set_at(index=index, value=value[k], key=k)
        else:
            if isinstance(index, (str, float)) or index < 0:
                raise ValueError(f"index must be integer in range from 0 upto length of array -1")
            if index > self.length():
                raise IndexError(f"index {index} out of range")
            self.set_at(index=index, value=value)

    def __delitem__(self, key):
        self.delete(key=key)

    def __count(self) -> int:
        """
        Count the length of Array instance
        :return: the count of items, 0 - in case of empty
        """
        item = self.__items
        length = 0
        while item:
            length += 1
            item = item.next
        return length

    def __add(self, val, key=None, n=1):
        prev_item = None if not self.__last else self.__last

        for index in range(0, n):
            item = Item(value=val, key=key, prev_item=prev_item)

            if not self.__items:
                self.__items = item
                prev_item = item
                self.__last = item
            else:
                prev_item.next = item
                prev_item = item
                self.__last = prev_item

        self.__length = self.__count()

    def __at(self, index=-1, key=None, value=None) -> Item:
        """
        Find and return an Item by index or first occurrence of item with specified key or value
        :param index:
        :param key:
        :param value:
        :return: Item or None
        """
        if index > self.__length // 2:
            item = self.__last
            n = self.__length - 1
            while item:
                if index == n or (key and key == item.key) or (value and value == item.value):
                    return item
                n -= 1
                item = item.prev
        else:
            item = self.__items
            n = 0
            while item:
                if index >= 0 and index == n:
                    return item
                if (key and key == item.key) or (value and value == item.value):
                    return item
                item = item.next
                n += 1

        return None

    def sort_by_value(self, e):
        return "" if e["value"] is None else e["value"]

    def sort_by_key(self, e):
        return "" if e["key"] is None else e["key"]

    def sort(self, reverse: bool = False, sort_by: str = "val"):
        """
        Sort an array by "val" or by "key" and return the new list with sorted elements
        :param reverse: True - ascending sort order, False - descending sort order
        :param sort_by: "val" - sort by values, "key" - sort by keys
        :return: the new list of sorted items in form: [{key:value},{key:value},...], or [value, value, ...]
        """
        list_to_sort = self.filter()
        if len(list_to_sort):
            if sort_by == "key":
                list_to_sort.sort(reverse=reverse, key=self.sort_by_key)
            else:
                list_to_sort.sort(reverse=reverse, key=self.sort_by_value)

            self.__sorted_list = list_to_sort
            return self.__sorted_list

    def get_sorted_list(self) -> List:
        """
        :return: return the previously sorted list
        """
        return self.__sorted_list

    def length(self) -> int:
        """
        Count the length of Array instance
        :return: the count of items, 0 - in case of empty
        """
        return self.__count()

    def set_at(self, index, value=None, key=None):
        """
        Set the value and key to item at specified index
        :param index: the index of item that will be changed
        :param value: optional parameter that will be stored
        :param key: optional parameter that will bbe stored
        :return: [bool] True in case of item was found and changed
        """
        item: Item = self.__at(index=index)
        if item:
            item.key = key if key else item.key
            item.value = value if value else item.value
            return True
        return False

    def insert(self, value, key=None, at_index=0):
        """
        Insert the new Item at specified position
        :param value: new Item value
        :param key: new Item key (optional)
        :param at_index: new Item position inside array, Default is 0
        :return: False in case of index is out of length
        """
        cur_item = self.__at(at_index)
        if cur_item is None:
            return False

        new_item = Item(value=value, key=key)

        if at_index == 0:
            new_item.next = self.__items
            new_item.next.prev = new_item
            self.__items = new_item
        else:
            new_item.next = cur_item
            new_item.prev = cur_item.prev
            new_item.prev.next = cur_item.prev = new_item

        self.__length = self.__count()
        return True

    def delete(self, at_index=-1, value=None, key=None):
        """
        Delete item from array. Item may be identified by its position, by value or by key
        In case of Item, specified by value or key only the first found item will be deleted
        :param at_index: an index of item that must be deleted
        :param value: the item with this value will be deleted
        :param key: the item with this ey will be deleted
        :return: False in case of out of index
        """
        del_item = self.__at(at_index, key=key, value=value)
        if del_item is None:
            return False

        if at_index == 0:
            self.__items = del_item.next
            del del_item
        else:
            del_item.prev.next = del_item.next
            if del_item.next:
                del_item.next.prev = del_item.prev
            else:
                self.__last = del_item.prev

            del del_item

        self.__length = self.__count()
        return True

    def index(self, value=None, key=None) -> int:
        """
        Find the index of first occurrence of item with specified value or key
        :param value: find item by value
        :param key: find value by key
        :return: an index of first occurrence of item or -1 in case of item not found
        """
        index = -1
        item = self.__items
        while item:
            if value and value == item.value:
                index += 1
                break
            if key and key == item.key:
                index += 1
                break
            item = item.next
            index += 1

        return index

    def value(self, index: int = -1, key=None):
        """
        Find and return the value of item specified by index or first occurrence of item, specified by key
        :param index: an index of item
        :param key: a key of item
        :return: value or None in case of item was not found
        """
        item = self.__at(index, key=key)
        if item is None:
            return None

        return item.value

    def key(self, index: int = -1, value=None):
        """
        Find and return the key of item specified by index or first occurrence of item, specified by value
        :param index: an index of item
        :param value: a value of item
        :return: key or None in case of item was not found or item has not key
        """
        item = self.__at(index, value=value)
        if item is None:
            return None

        return item.key

    def at(self, index: int = -1, key=None, value=None):
        """
        Find an item by specified parameter and return the {key: value} or value in case of key is None
        :param index: return an item by specified index
        :param key: return the first occurrence of item with specified key
        :param value: return the first occurrence of item with specified value
        :return: the dict of item parameters: key and value in form {item.key: item.value}, or just the value in
        case of key is None, or empty string in case of item was not found
        """
        item = self.__at(index, key=key, value=value)
        if item is None:
            return ""

        return item.get()

    def filter(self, by_value=None, by_key=None) -> List[{}]:
        """
        Finds all concurrences specified by key or by value, builds and
        returns the list of pairs in form [{key:value}, {key:value}, ...],
        one of two arguments must be specified!

        :param by_value: [any] find all concurrences by specified value
        :param by_key: [any]  find all concurrences by specified key

        :return: List: the list of pairs in form [{key:value}, {key:value}, ...],
            or empty list in case of no one items was found

        Example
                print(arr.filter(by_key="key")
        """
        filtered = []
        item = self.__items
        while item:
            if by_key and by_key == item.key:
                filtered.append({item.key: item.value})
            if by_value and by_value == item.value:
                filtered.append({item.key: item.value})
            if by_key is None and by_value is None:
                filtered.append({"key": item.key, "value": item.value})
            item = item.next
        return filtered

    def scopy(self):
        """
        Returns the safe copy of this array
        :return:
            Array: the copy of current instance of Array class
        """
        new_arr = Array()
        item = self.__items
        while item:
            new_arr.append(item.value, key=item.key)
            item = item.next
        return new_arr

    def append(self, val, key=None, count: int = 1) -> int:
        """
        Append the new item at the end of Array instance
        :param val: [any] - the value
        :param key: [any] - optional parameter
        :param count: [int] - optional parameter, the count of items to be appended
        :return: the new length of array
        """
        self.__add(val=val, key=key, n=count)
        return self.length()


if __name__ == "__main__":
    test_array = Array()
    for i in range(0, 100):
        test_array.append(i, f"k.{i}")

    print(test_array)
    print(test_array.index(value=50))
    print(test_array.index(key="k.50"))
    print(test_array.length())
    print(test_array.delete(50))
    print(test_array.length())

    if test_array.set_at(10, 100, key="k.100"):
        print(test_array)

    arr_copy = test_array.scopy()
    print(arr_copy)
    arr_copy.set_at(20, 100, key="k.20")
    arr_copy.set_at(30, 100, key="k.20")
    arr_copy.set_at(40, 100, key="k.20")
    arr_copy.set_at(50, 100, key="k.20")

    fv100 = arr_copy.filter(by_value=100)
    fk20 = arr_copy.filter(by_key="k.20")
    print(fv100, " : ", fk20)

    to_be_sorted = Array()
    for i in range(0, 10):
        to_be_sorted.append(10-i)

    print("sort by value, ascending:", to_be_sorted.sort(reverse=False))
    print("sort by value, descending", to_be_sorted.sort(reverse=True))
    print("sort by key, ascending", to_be_sorted.sort(reverse=False, sort_by="key"))
    print("sort by key, descending", to_be_sorted.sort(reverse=True, sort_by="key"))

    for i in arr_copy:
        v = i

    myit = iter(fv100)
    print(next(myit))
    print(next(myit))
    print(next(myit))
    print(next(myit))

    #   create Array from list
    arr = ["banana", "orange", "kiwi"]
    fruits = Array(from_list=arr)
    print(f"fruits length is: {fruits.length()}: {fruits}")

    #   create Array from dict
    dobj = {"k1": "banana", "k2": "orange", "k3": "kiwi"}
    fruits_arr = Array(from_list=arr, from_dict=dobj)
    print(f"fruits length is: {fruits_arr.length()}: {fruits_arr}")

    fruits[0] = arr_copy[0]
    fruits[1] = {"k1": 1}
    fruits.append("pineapple")
    fruits.append("lemon")
    fruits.insert("tomatoes", at_index=4)
    print(fruits)
    fruits.delete(0)
    print(fruits)
    # fruits[1000] = 0  # IndexException

    count = fruits.length()
    fruits.delete(count-1)

    count = fruits.length()
    print(fruits.value(count-2))
