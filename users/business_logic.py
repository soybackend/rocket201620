# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from users.models import Artist, BusinessAgent, TokenUser
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.mail import send_mail


#     get_info_users
#     Este médodo permite retornar todos los usuarios
#     Param: GET.


def get_info_users(request):
    if request.method == 'GET':
        users = []

        users_all = User.objects.all()

        for user in users_all:
            users.append(user_to_json(user))

        return users


# user_to_json
#     Este médodo permite transformar un usuario en json
#     Param: usuario.


def user_to_json(user):
    json_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

    return json_data


#     register_user_in_model
#     Este médodo permite registrar un usuario
#     Param: datos del usuario.


def register_user_in_model(json_data):
    first_name = json_data['first_name']
    last_name = json_data['last_name']
    username = json_data['username']
    password1 = json_data['password1']
    password2 = json_data['password2']
    email = json_data['email']
    is_artist = json_data['is_artist']

    is_artist = str_to_bool(is_artist)

    if (username != "" and password1 != "" and password2 != "" and
       email != "" and first_name != "" and last_name != ""):

        exist_user = User.objects.filter(username=username)

        if exist_user.count() > 0:
            status = 'Usuario ya existe.'
        else:
            if password1 != password2:
                status = 'Las contrasenias no coinciden.'
            else:
                user_model = User.objects.create_user(username=username,
                                                      password=password1,
                                                      email=email,
                                                      first_name=first_name,
                                                      last_name=last_name)
                user_model.save()

                if is_artist is False:
                    status = 'OK'
                else:
                    if is_artist:
                        if relation_user_to_artist(user_model, json_data):
                            status = 'OK'
                        else:
                            status = 'Error guardando el perfil del usuario'
                            status = status + ' como artista'''
    else:
        status = 'Todos los campos son obligatorios.'

    return {'status': status}


#     str_to_bool
#     Este médodo permite transformar un str a bool
#     Param: str


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError


# relation_user_to_artist
#     Este médodo permite asociar al modelo de usuario, el perfil delartista.
#     Param: usuario, datos del perfil


def relation_user_to_artist(user_model, json_data):
    user_artist = Artist()

    artistic_name = json_data['artistic_name']
    # avatar = request.FILES['avatar']
    bank_account_number = json_data['bank_account_number']
    bank_account_type = json_data['bank_account_type']
    bank = json_data['bank']
    address = json_data['address']
    city = json_data['city']
    country = json_data['country']
    telephone_number = json_data['telephone_number']
    birth_date = json_data['birth_date']

    user_artist.artistic_name = artistic_name
    user_artist.avatar = ""
    user_artist.bank_account_number = bank_account_number
    user_artist.bank_account_type = bank_account_type
    user_artist.bank = bank
    user_artist.address = address
    user_artist.city = city
    user_artist.country = country
    user_artist.telephone_number = telephone_number
    user_artist.birth_date = birth_date

    user_artist.user = user_model

    user_artist.save()

    return True


#     login_service
#     Este médodo permite registrar un usuario
#     Param: datos del usuario.


def login_service(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if (username is not None and password is not None):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return login_user_to_json(user)
        else:
            status = 'Usuario o clave incorrecta.'
    else:
        status = 'Todos los campos son obligatorios.'
    return {'status': status}


#     login_user_to_json
#     Este médodo permite transformar un usuario autenticado en json
#     Param: usuario.


def login_user_to_json(user):
    # Is Artist
    try:
        artist = Artist.objects.get(user__id=user.id)
        is_artist = True
        id_artist = artist.id
    except:
        is_artist = False
        id_artist = -1
    # Is Business Agent
    try:
        agent = BusinessAgent.objects.get(user__id=user.id)
        id_agent = agent.id
    except:
        id_agent = -1
    # Generate Token
    try:
        token = Token.objects.create(user=user)
    except:
        token = Token.objects.get(user__id=user.id)

    json_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'token': token.key,
        'is_artist': is_artist,
        'id_user': user.id,
        'id_artist': id_artist,
        'id_agent': id_agent
    }
    return json_data


def business_agent_create_action(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if (username is not "" and password1 is not "" and password2 is not "" and
       email is not "" and first_name is not "" and
       last_name is not ""):

        exist_user = User.objects.filter(username=username)
        if exist_user.count() > 0:
            status = 'Usuario ya existe.'
        else:
            if password1 != password2:
                status = 'Las contraseñas no coinciden.'
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)
                user.save()

                if business_agent_create_subaction(user, request):
                    status = ''
                else:
                    status = 'Error guardando el agente comercial.'
    else:
        status = 'Todos los campos son obligatorios.'
    return status


def business_agent_create_subaction(user, request):
    agent = BusinessAgent()

    agent.telephone_number = request.POST.get('telephone_number')
    agent.avatar = request.POST.get('avatar')
    agent.address = request.POST.get('address')
    agent.city = request.POST.get('city')
    agent.country = request.POST.get('country')
    agent.user = user

    agent.save()
    return True


def business_agent_update_action(request, id_user):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')

    print(id_user)

    if (email is not "" and first_name is not "" and last_name is not ""):

        user = User.objects.get(id=id_user)
        if user is None:
            status = 'Usuario no existe.'
        else:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if business_agent_update_subaction(user, request):
                status = ''
            else:
                status = 'Error guardando el agente comercial.'
    else:
        status = 'Todos los campos son obligatorios.'
    return status


def business_agent_update_subaction(user, request):
    agent = BusinessAgent.objects.get(user__id=user.id)

    agent.telephone_number = request.POST.get('telephone_number')
    agent.avatar = request.POST.get('avatar')
    agent.address = request.POST.get('address')
    agent.city = request.POST.get('city')
    agent.country = request.POST.get('country')
    agent.birth_date = request.POST.get('birth_date')
    agent.user = user

    agent.save()
    return True


def request_password_restore_action(request):
    username = request.GET.get('username')

    if username is not None:
        try:
            user = User.objects.get(username=username)
            if user is not None:
                if request_password_restore_subaction(user, request):
                    status = 'Correo enviado.'
                else:
                    status = 'Error en el envio del correo.'
            else:
                status = 'Usuario no existe.'
        except:
            status = 'Parece que el usuario no existe.'
    else:
        status = 'No se envío un username.'

    return {'status': status}


def request_password_restore_subaction(user, request):
    try:
        dto = TokenUser.objects.get(user__id=user.id)
    except:
        dto = TokenUser()
        dto.user = user
        dto.save()

    try:
        subject = 'Freeven :: Servicio de recuperación de contraseña'
        body_text = 'Estimado ' + user.first_name + ', \n\n'
        body_text = body_text + 'Para recuperar su clave haga clic en el '
        body_text = body_text + 'siguiente enlace: \n\n'
        body_text = body_text + 'http://' + request.META['HTTP_HOST']
        body_text = body_text + '#/user/pass/restore/yRQYnWzskCZUxPwaQupWkiUzKELZ49eM7oWxAQK_ZXw/' + str(user.id)
        body_text = body_text + '\n\n Cordial saludo,'

        send_mail(subject, body_text, settings.EMAIL_HOST_USER,
                  [user.email], fail_silently=True)
        return True
    except:
        return False


def change_password_action(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if (username is not None and password is not None):
        try:
            user = User.objects.get(username=username)
            try:
                token_user = TokenUser.objects.get(user__id=user.id)
                user.set_password(password)
                user.save()
                token_user.delete()
                status = 'La clave fue actualizada.'
            except:
                status = 'El token no existe, debe solicitar el cambio de '
                status = status + 'clave.'
        except:
            status = 'Usuario no existe.'
    else:
        status = 'Todos los campos son obligatorios.'
    return {'status': status}


def change_password_op_action(request):
    username = request.GET.get('username')
    password = request.GET.get('password1')
    old_password = request.GET.get('password')

    if (username is not None and password is not None and
       old_password is not None):
        user = authenticate(username=username, password=old_password)
        if user is not None:
            user.set_password(password)
            user.save()
            status = 'La clave fue actualizada.'
        else:
            status = 'Usuario o clave  incorrecta.'
    else:
        status = 'Todos los campos son obligatorios.'
    return {'status': status}


def update_profile_action(json_data):
    first_name = json_data.GET['first_name']
    last_name = json_data.GET['last_name']
    username = json_data.GET['username']
    email = json_data.GET['email']

    status = ''

    if (username != "" and email != "" and first_name != "" and
       last_name != ""):

        user = User.objects.get(username=username)

        if user is not None:

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            status = 'Datos de usuario actualizados.'

        else:
            status = 'Usuario no existe.'
    else:
        status = 'Todos los campos son obligatorios.'

    return {'status': status}


def update_profile_agent_action(user, json_data):
    try:
        agent = BusinessAgent.objets.get(user__id=user.id)

        agent.address = json_data['address']
        agent.city = json_data['city']
        agent.country = json_data['country']
        agent.telephone_number = json_data['telephone_number']
        agent.save()
        status = 'Datos del perfil del agente comercial fueron actualizados.'
    except:
        status = 'Error guardando el perfil del agente comercial'
    return {'status': status}


def update_profile_artist_action(user, json_data):
    try:
        artist = Artist.objects.filter(user__id=user.id)
        artist.update(artistic_name=json_data.POST['artistic_name'])
        artist.update(
            bank_account_number=json_data.POST['bank_account_number'])
        artist.update(bank_account_type=json_data.POST['bank_account_type'])
        artist.update(bank=json_data.POST['bank'])
        artist.update(address=json_data.POST['address'])
        artist.update(city=json_data.POST['city'])
        artist.update(country=json_data.POST['country'])
        artist.update(telephone_number=json_data.POST['telephone_number'])
        artist.update(birth_date=json_data.POST['birth_date'])
        artist.save()
        status = 'Datos del perfil del artista fueron actualizados.'
    except:
        status = 'Error guardando el perfil del artista'
    return {'status': status}
