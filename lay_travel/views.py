from datetime import date
from rest_framework.response import Response
from rest_framework.views import APIView, status
from .models import PostLocation, Image, UserPost, MainPlace, Package, PackagePlace
from django.contrib.gis.geos import Point
from .serializers import UserPostSerializer, MainPlaceSerializer, PostLocationSerializer, PackageSerializer
from django.db.models import Max
from rest_framework.permissions import IsAuthenticated
import json
from django.db.models import Q


# Create your views here.
response_txt_key = 'message'


class HomeView(APIView):

    def get(self, request):
        return Response({
            response_txt_key: 'Welcome to Gis Work! Travel with us'
        })


class LayTravllerPostView(APIView):

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        else:
            return []

    def get(self, request):

        try:
            main_place = request.GET.get("main_place")
            main_place_information = MainPlace.objects.get(
                place_name=main_place.upper())
            if not main_place_information:
                return Response(status=status.HTTP_404_NOT_FOUND)
            places = PostLocation.objects.filter(
                main_place__id=main_place_information.id)
            user_post = UserPost.objects.filter(
                main_place_id=main_place_information.id)

            locations = []
            for place in places:
                location = {
                    "srid": place.geo_location.srid,
                    "points": {
                        "latitude": place.geo_location[0],
                        "longitude": place.geo_location[1]
                    }
                }
                locations.append(location)

            serializer = PostLocationSerializer(places, many=True)
            data = serializer.data

            user_postSerializer = UserPostSerializer(user_post, many=True)
            user_post_data = user_postSerializer.data

            for idx, _ in enumerate(data):
                data[idx]['geo_location'] = locations[idx]
                data[idx]['images'] = Image.objects.filter(
                    post_location__id=data[idx]['id']).values('image_post')
                data[idx]['day'] = user_post_data[idx]["day"]
                data[idx]['user'] = user_post_data[idx]["user"]
                data[idx]['main_place_id'] = user_post_data[idx]["main_place_id"]

            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        # str/text data handling
        request_raw_data = dict(request.data)
        request_require_data = request_raw_data['data'][0]
        request_filter_data = json.loads(request_require_data)

        # image data handling
        request_raw_data.pop('data')
        request_image_data = request_raw_data

        try:
            for idx, _ in enumerate(request_filter_data):

                day = request_filter_data[idx]['day']
                place_name = request_filter_data[idx]['place_name']
                location_name = request_filter_data[idx]['location_name']
                geo_location = request_filter_data[idx]['geo_location']
                images = request_image_data[f"image_post[{idx}][{geo_location}]"]

                is_data_available = place_name and location_name and geo_location and images

                if is_data_available:
                    primary_instance = ''
                    place_name = place_name.upper()

                    try:
                        primary_instance = MainPlace.objects.get(
                            place_name=place_name)
                    except MainPlace.DoesNotExist:
                        main_place_record = MainPlaceSerializer(
                            data={'place_name': place_name})
                        if main_place_record.is_valid():
                            primary_instance = main_place_record.save()
                        else:
                            return Response({'msg': 'Main Place is not valid'})

                    post_location_instance = PostLocation(
                        main_place=primary_instance, location_name=location_name)
                    geo_location_data = geo_location.split(",")
                    post_location_instance.geo_location = Point(
                        float(geo_location_data[0]), float(geo_location_data[1]))
                    post_location_instance.save()

                    for image in images:
                        Image.objects.create(
                            post_location=post_location_instance, image_post=image)
                else:
                    return Response({response_txt_key: "Fields can't be empty!"})

                request_filter_data[idx]['user'] = request.user.id
                request_filter_data[idx]['main_place_id'] = primary_instance.id
                new_user_post = UserPostSerializer(
                    data=request_filter_data[idx])

                is_valid_and_exists = new_user_post.is_valid(
                ) and request_filter_data[idx]['user']

                if is_valid_and_exists:
                    new_user_post.save()
                else:
                    return Response({response_txt_key: "Data is not valid"})
            return Response({response_txt_key: 'Data insertion successful'})
        except Exception as e:
            print(f"Error while insertion {e}")
            return Response({response_txt_key: f'Data insertion failed {e}'})


class LayTravellerPlaceView(APIView):
    def get(self, request):
        main_place_list = MainPlace.objects.all()

        try:
            serializer = MainPlaceSerializer(main_place_list, many=True)
            data = serializer.data

            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as e:
            print(f"Error while getting data")
            return Response({response_txt_key: f'Data insertion failed {e}'})


class ItineraryPackageView(APIView):
    def get(self, request):
        try:
            id = request.GET.get('user_id')
            user_post_raw = UserPost.objects.filter(user_id=id)
            itinerary_data = []
            main_place_ids = []

            for user_post in user_post_raw:
                main_id = user_post.main_place_id
                if main_id not in main_place_ids:
                    main_place_ids.append(main_id)

            for idx, _ in enumerate(main_place_ids):
                main_place_information = MainPlace.objects.get(
                    id=main_place_ids[idx])
                if not main_place_information:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                places = PostLocation.objects.filter(
                    main_place__id=main_place_information.id)
                user_post = UserPost.objects.filter(
                    main_place_id=main_place_information.id)

                locations = []
                for place in places:
                    location = {
                        "srid": place.geo_location.srid,
                        "points": {
                            "latitude": place.geo_location[0],
                            "longitude": place.geo_location[1]
                        }
                    }
                    locations.append(location)

                serializer = PostLocationSerializer(places, many=True)
                data = serializer.data

                user_postSerializer = UserPostSerializer(user_post, many=True)
                user_post_data = user_postSerializer.data

                for idy, _ in enumerate(data):
                    data[idy]['day'] = user_post_data[idy]["day"]
                    data[idy]['geo_location'] = locations[idy]
                    data[idy]['images'] = Image.objects.filter(
                        post_location__id=data[idy]['id']).values('image_post')

                main_place_data = {
                    'main_place': main_place_information.place_name.lower(),
                    'main_place_id': main_place_information.id,
                    'travelled_place': len(data),
                    'data': data
                }

                itinerary_data.append(main_place_data)

            return Response(status=status.HTTP_200_OK, data=itinerary_data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)


# api to strore unique package name and other data
class LayTravelerUniquePackageNamePackagePostView(APIView):

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        else:
            return []

    def get(self, request):
        try:
            package_name = request.GET.get('package_name')
            package_name = package_name.upper()
            user_post_raw = UserPost.objects.filter(package_name=package_name)

            itinerary_data = []
            main_place_ids = []
            package_names = []

            for user_post in user_post_raw:
                main_id = user_post.main_place_id
                if main_id not in main_place_ids:
                    main_place_ids.append(main_id)

            for idx, _ in enumerate(main_place_ids):
                main_place_information = MainPlace.objects.get(
                    id=main_place_ids[idx])
                if not main_place_information:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                places = PostLocation.objects.filter(
                    main_place__id=main_place_information.id)
                user_post = UserPost.objects.filter(
                    main_place_id=main_place_information.id)

                locations = []
                for place in places:
                    location = {
                        "srid": place.geo_location.srid,
                        "points": {
                            "latitude": place.geo_location[0],
                            "longitude": place.geo_location[1]
                        }
                    }
                    locations.append(location)

                serializer = PostLocationSerializer(places, many=True)
                data = serializer.data

                user_postSerializer = UserPostSerializer(user_post, many=True)
                user_post_data = user_postSerializer.data

                for idy, _ in enumerate(data):
                    data[idy]['day'] = user_post_data[idy]["day"]
                    data[idy]['geo_location'] = locations[idy]
                    data[idy]['images'] = Image.objects.filter(
                        post_location__id=data[idy]['id']).values('image_post')

                main_place_data = {
                    'main_place': main_place_information.place_name.lower(),
                    'main_place_id': main_place_information.id,
                    'travelled_place': len(data),
                    'data': data
                }

                itinerary_data.append(main_place_data)

            return Response(status=status.HTTP_200_OK, data=itinerary_data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        # str/text data handling
        request_raw_data = dict(request.data)
        request_require_data = request_raw_data['data'][0]
        request_package_name = request_raw_data['package_name'][0]
        request_filter_data = json.loads(request_require_data)

        # image data handling
        request_raw_data.pop('data')
        request_image_data = request_raw_data

        # package name to be inserted
        package_name = request_package_name

        try:
            for idx, _ in enumerate(request_filter_data):

                day = request_filter_data[idx]['day']
                place_name = request_filter_data[idx]['place_name']
                location_name = request_filter_data[idx]['location_name']
                geo_location = request_filter_data[idx]['geo_location']
                images = request_image_data[f"image_post[{idx}][{geo_location}]"]

                is_data_available = place_name and location_name and geo_location and images

                if is_data_available:
                    primary_instance = ''
                    place_name = place_name.upper()
                    package_name = package_name.upper()

                    try:
                        primary_instance = MainPlace.objects.get(
                            place_name=place_name)
                    except MainPlace.DoesNotExist:
                        main_place_record = MainPlaceSerializer(
                            data={'place_name': place_name})
                        if main_place_record.is_valid():
                            primary_instance = main_place_record.save()
                        else:
                            return Response({'msg': 'Main Place is not valid'})

                    package_instance = Package(
                        main_place=primary_instance, package_name=package_name)
                    package_instance.save()
                    post_location_instance = PostLocation(
                        main_place=primary_instance, location_name=location_name)
                    geo_location_data = geo_location.split(",")
                    post_location_instance.geo_location = Point(
                        float(geo_location_data[0]), float(geo_location_data[1]))
                    post_location_instance.save()

                    for image in images:
                        Image.objects.create(
                            post_location=post_location_instance, image_post=image)
                else:
                    return Response({response_txt_key: "Fields can't be empty!"})

                request_filter_data[idx]['user'] = request.user.id
                request_filter_data[idx]['main_place_id'] = primary_instance.id

                # addition of package name details or datas here
                request_filter_data[idx]['package_name'] = package_name.upper()
                new_user_post = UserPostSerializer(
                    data=request_filter_data[idx])

                is_valid_and_exists = new_user_post.is_valid(
                ) and request_filter_data[idx]['user']

                if is_valid_and_exists:
                    new_user_post.save()
                else:
                    return Response({response_txt_key: "Data is not valid"})
            return Response({response_txt_key: 'Data insertion successful'})
        except Exception as e:
            print(f"Error while insertion {e}")
            return Response({response_txt_key: f'Data insertion failed {e}'})


# test package for api creation:

class PackageInformationView(APIView):
    def get(self, request):
        try:
            package_name = request.GET.get('package_name')
            upper_package_name = package_name.upper()

            # filter packages with similar package names
            query_packages = Package.objects.filter(
                Q(package_name__startswith=upper_package_name) | Q(
                    package_name__istartswith=upper_package_name)
            ).order_by('package_name')

            # create a dictionary of package objects
            packages = {index: {'id': package.id, 'package_name': package.package_name}
                        for index, package in enumerate(query_packages)}

            # packages informations dict
            package_info = {}
            itinerary_infos = []


            # filter packages id from the user's query.
            packages_ids = []
            for package_index in packages:
                package_id = packages[package_index]['id']
                if package_id not in packages_ids:
                    packages_ids.append(package_id)

            # filter places ids associated with the package
            for package_id_itr in packages_ids:
                package_places = PackagePlace.objects.filter(
                    package_id=package_id_itr)
                main_place_ids = []
                for place in package_places:
                    main_place_id = place.main_place_id
                    if main_place_id not in main_place_ids:
                        main_place_ids.append(main_place_id)

                # store main places ids associated to the unique package.
                key = str(package_id_itr)
                value = main_place_ids
                package_info[key] = value

            # iterate over the packages data
            for key, value in package_info.items():
                package_contributers=[]
                package_instance = Package.objects.get(id=int(key))
                package_name = package_instance.package_name.title()
                main_place_infos = []

                for main_place_itr in value:
                    main_place_instance = MainPlace.objects.get(
                        id=main_place_itr)


                    places =[]
                    user_post_filtered = UserPost.objects.filter(main_place_id=main_place_itr)
                    for user_post in user_post_filtered:
                        user_id = user_post.user_id
                        if user_id not in package_contributers:
                            package_contributers.append(user_id)

                        location_place = PostLocation.objects.get(user_post__id = user_post.id)
                        place = location_place.location_name.title()
                        if place not in places:
                            places.append(place)

                    main_place_data = {
                        'id': main_place_instance.id,
                        'name': main_place_instance.place_name.title(),
                        'places':places
                    }
                    main_place_infos.append(main_place_data)

                package_data = {
                    'package_id': int(key),
                    'package_name': package_name,
                    'main_places': main_place_infos,
                    'contributor':package_contributers
                }
                itinerary_infos.append(package_data)

            itinerary_data = {
                'data_size' : len(itinerary_infos),
                'data' : itinerary_infos
            }
            return Response(status=status.HTTP_200_OK, data=itinerary_data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            # Extract required data from request
            request_raw_data = dict(request.data)
            request_require_data = request_raw_data['data'][0]
            request_package_name = request_raw_data['package_name'][0]
            request_filter_data = json.loads(request_require_data)
            request_raw_data.pop('data')
            request_image_data = request_raw_data

            # Save user posts
            for idx, filter_data in enumerate(request_filter_data):
                # Extract required fields from filter_data
                day = filter_data['day']
                place_name = filter_data['place_name'].upper()
                location_name = filter_data['location_name']
                geo_location = filter_data['geo_location']
                images = request_image_data[f"image_post[{idx}][{geo_location}]"]

                # Check if all required fields are present
                if not all([place_name, location_name, geo_location, images]):
                    return Response({'msg': 'Fields can\'t be empty!'})

                # Get or create related objects
                primary_instance_package, _ = Package.objects.get_or_create(
                    package_name=request_package_name.upper())
                print(f"Primary instance package {primary_instance_package}")


                primary_instance_main_place, _ = MainPlace.objects.get_or_create(
                    place_name=place_name)

                # Save package_place_instance
                try:
                    package_place_instance = PackagePlace.objects.get(
                        package=primary_instance_package, main_place=primary_instance_main_place)
                except PackagePlace.DoesNotExist:
                    package_place_instance = PackagePlace.objects.create(
                        package=primary_instance_package, main_place=primary_instance_main_place)

                # Save user post instance
                filter_data['user'] = request.user.id
                filter_data['main_place_id'] = primary_instance_main_place.id
                filter_data['package_id']  = primary_instance_package.id
                new_user_post = UserPostSerializer(data=filter_data)

                if new_user_post.is_valid():
                    user_post_instance = new_user_post.save()
                    # Save post_location_instance
                    post_location_instance = PostLocation.objects.create(
                        user_post=user_post_instance, location_name=location_name, geo_location=Point(*map(float, geo_location.split(","))))
                    # Save image instances
                    for image in images:
                        Image.objects.create(
                            post_location=post_location_instance, image_post=image)
                else:
                    return Response({'msg': 'User post data is not valid'})

            return Response({'msg': 'Data insertion successful'})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    # def post(self, request):

        # str/text data handling
        request_raw_data = dict(request.data)
        request_require_data = request_raw_data['data'][0]
        request_package_name = request_raw_data['package_name'][0]
        request_filter_data = json.loads(request_require_data)

        # image data handling
        request_raw_data.pop('data')
        request_image_data = request_raw_data

        # package name to be inserted
        package_name = request_package_name

        try:
            for idx, _ in enumerate(request_filter_data):

                day = request_filter_data[idx]['day']
                place_name = request_filter_data[idx]['place_name']
                location_name = request_filter_data[idx]['location_name']
                geo_location = request_filter_data[idx]['geo_location']
                images = request_image_data[f"image_post[{idx}][{geo_location}]"]

                primary_instance_main_place = ''
                primary_instance_package = ''

                is_data_available = place_name and location_name and geo_location and images

                if is_data_available:
                    place_name = place_name.upper()
                    package_name = package_name.upper()

                    try:
                        primary_instance_package = Package.objects.get(
                            package_name=package_name)
                        primary_instance_main_place = MainPlace.objects.get(
                            place_name=place_name)

                    except Package.DoesNotExist:
                        package_record = PackageSerializer(
                            data={'package_name': package_name})
                        if (package_record.is_valid):
                            primary_instance_package = package_record.save()
                        else:
                            return Response({'msg': 'Package is not valid'})
                    except MainPlace.DoesNotExist:

                        main_place_record = MainPlaceSerializer(
                            data={'place_name': place_name})
                        if main_place_record.is_valid():
                            primary_instance_main_place = main_place_record.save()
                        else:
                            return Response({'msg': 'Main Place is not valid'})

                    # primary_instance_package => save
                    primary_instance_package = Package(
                        package_name=package_name)

                    if primary_instance_package.is_valid():
                        primary_instance_package.save()
                    else:
                        return Response({'msg': 'Package data is not valid'})

                    # primary_instance_package => save
                    primary_instance_main_place = MainPlace(
                        place_name=place_name)
                    if primary_instance_main_place.is_valid():
                        primary_instance_main_place.save()
                    else:
                        return Response({'msg': 'Main place data is not valid'})

                    # primary_instance_package_place => save
                    package_place_instance = PackagePlace(
                        package=primary_instance_package, main_place=primary_instance_main_place)

                    if package_place_instance.is_valid():
                        package_place_instance.save()
                    else:
                        return Response({'msg': 'Package place item is not'})

                    request_filter_data[idx]['user'] = request.user.id
                    request_filter_data[idx]['main_place_id'] = primary_instance_main_place.id

                    # addition of package name details or datas here
                    request_filter_data[idx]['package_name'] = package_name.upper(
                    )
                    new_user_post = UserPostSerializer(
                        data=request_filter_data[idx])

                    is_valid_and_exists = new_user_post.is_valid(
                    ) and request_filter_data[idx]['user']

                    if is_valid_and_exists:
                        user_post_instance = new_user_post.save()
                        post_location_instance = PostLocation(
                            user=user_post_instance, location_name=location_name)
                        geo_location_data = geo_location.split(",")
                        post_location_instance.geo_location = Point(
                            float(geo_location_data[0]), float(geo_location_data[1]))
                        post_location_instance.save()

                        for image in images:
                            Image.objects.create(
                                post_location=post_location_instance, image_post=image)
                    else:
                        return Response({response_txt_key: "User post data is not valid"})

                else:
                    return Response({response_txt_key: "Fields can't be empty!"})

            return Response({response_txt_key: 'Data insertion successful'})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)



class UserItineraryInformationView(APIView):

    def get(self, request):

        query_dict = {}

        try:
            # query_params = request.GET
            # for key, value in query_params.items():
            #     query_dict[key]= value

            # user_id = query_dict['user_id']
            # package_id = query_dict['package_id']

            user_id = request.GET.get('user_id')
            user_post_raw = UserPost.objects.filter(user_id=user_id)
            itinerary_data = []
            main_place_ids = []

            for user_post in user_post_raw:
                main_id = user_post.main_place_id
                if main_id not in main_place_ids:
                    main_place_ids.append(main_id)

            print(f"Main places id = {main_place_ids}")

            for idx, _ in enumerate(main_place_ids):
                main_place_id = main_place_ids[idx]
                main_place_information = MainPlace.objects.get(id=main_place_id)
                if not main_place_information:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                user_posts = UserPost.objects.filter(main_place_id=main_place_information.id)
                print(f"User post length= {len(user_posts)}")
                for user_post in user_posts:
                    places = PostLocation.objects.filter(user_post_id=user_post.id)
                    locations = []
                    for place in places:
                        location = {
                        "srid": place.geo_location.srid,
                        "points": {
                            "latitude": place.geo_location[0],
                            "longitude": place.geo_location[1]
                            }
                        }
                        locations.append(location)

                    serializer = PostLocationSerializer(places, many=True)
                    data = serializer.data

                    user_post_serializer = UserPostSerializer(user_posts,many=True)
                    user_post_data = user_post_serializer.data

                    for idk,_ in enumerate(data):
                        data[idk]['day'] = user_post_data[idk]["day"]
                        data[idk]['geo_location'] = locations[idk]
                        data[idk]['images'] = Image.objects.filter(post_location__id=data[idk]['id']).values('image_post')

                main_place_data = {
                    'main_place': main_place_information.place_name.lower(),
                    'main_place_id': main_place_information.id,
                    'travelled_place': len(data),
                    'data': data
                }


                # user_postSerializer = UserPostSerializer(user_post, many=True)
                # user_post_data = user_postSerializer.data

                # for idy, _ in enumerate(data):
                #     data[idy]['day'] = user_post_data[idy]["day"]
                #     data[idy]['geo_location'] = locations[idy]
                #     data[idy]['images'] = Image.objects.filter(
                #         post_location__id=data[idy]['id']).values('image_post')

                # main_place_data = {
                #     'main_place': main_place_information.place_name.lower(),
                #     'main_place_id': main_place_information.id,
                #     'travelled_place': len(data),
                #     'data': data
                # }

                itinerary_data.append(main_place_data)

            return Response(status=status.HTTP_200_OK, data=itinerary_data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        pass