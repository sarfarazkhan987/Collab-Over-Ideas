from passlib.handlers.pbkdf2 import pbkdf2_sha256

from collaboverideas.models import User, Country


def add_user(firstname, username, password, email):
    hashed_password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    query = User(username=username, firstname=firstname, password=hashed_password, email=email)
    query.save()


def check_user(username, password):
    if User.objects.filter(username__iexact=username).exists():
        user = User.objects.get(username__iexact=username)
        hashed_password = user.password
        return pbkdf2_sha256.verify(password, hashed_password)
    else:
        return False


def check_username(username):
    return User.objects.filter(username__iexact=username).exists()


def get_user(username):
    return User.objects.filter(username__iexact=username).values()[0]


def get_user_id(username):
    user = User.objects.get(username=username)
    return user.id


def get_country_name(country_id):
    if country_id is None:
        return ''
    country_name = Country.objects.get(id=country_id)
    return country_name

def update_user(username, firstname, lastname, email, dob, password, country):
    print("previous user name" + lastname)
    # print("countryname"+country)
    # print("dob is"+dob)
    if country == '':
        c_id = ''
    else:
        if Country.objects.filter(country_name__iexact=country).exists():
            country = Country.objects.get(country_name__iexact=country)
            c_id = country.id
        else:
            query1 = Country(country_name=country)
            query1.save()
            # print(query1)
            country = Country.objects.get(country_name__iexact=country)

            # print(country)
            c_id = country.id
    hashed_password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    query = User.objects.filter(username=username).update(password=hashed_password, firstname=firstname,
                                                          lastname=lastname,
                                                          email=email, dob=dob, country_id=c_id)

    return query



