class PhoneNumber(object):
    class Invalid(Exception):
        pass

    def __init__(self, text, int_prefix='+32'):
        self.int_prefix = int_prefix
        self.number = str(text)
        if self.number[0] == '+':
            self.int_prefix = self.number[:3]
            self.number = self.number[3:]
        elif self.number[0] == '0':
            self.number = self.number[1:]

        if not self.number.isdigit():
            raise self.Invalid(text)

    def __str__(self):
        return self.int_prefix + self.number

    def __repr__(self):
        res = str(self)
        return ' '.join((res[:3], res[3:6], res[6:8], res[8:10], res[10:]))
        
    def is_belgian_gsm(self):
        return (
            self.int_prefix == '+32' and 
            self.number[0] == '4' and 
            self.number[1] in ('7', '8', '9') and
            len(self.number) == 9
        )
