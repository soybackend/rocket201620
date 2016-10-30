# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from tracks.models import Track, RateTrack
from django.db.models import Avg


def register_rate_track_action(request):
    username = request.GET.get('username')
    track_id = request.GET.get('track_id')
    rate = request.GET.get('rate')

    if (username is not None and password is not None and rate is not None):
        try:
            if(int(rate) < 1 or int(rate) > 5):
                status = 'Calificacion no valida.'
            else:
                try:
                    user = User.objects.get(username=username)
                    try:
                        track = Track.objects.get(id=track_id)

                        r_track = RateTrack()
                        r_track.user = user
                        r_track.track = track
                        r_track.rate = rate
                        r_track.save()

                        count_votes = RateTrack.objects.count(
                            track__id=track.id)
                        score = RateTrack.objects.filters(
                            track__id=track.id).aggregate(Avg('rate'))

                        track.score = score
                        track.count_votes = count_votes

                        status = 'La calificacion fue registrada.'
                    except:
                        status = 'La obra musical no existe.'
                except:
                    status = 'Usuario no existe.'
        except:
            status = 'Error en formato de calificacion.'
    else:
        status = 'Todos los campos son obligatorios.'
    return {'status': status}
