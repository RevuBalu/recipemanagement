from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from recipes.models import Recipe

from recipes.serializers import RecipeSerializer

from recipes.serializers import UserSerializer

from recipes.models import Review

from recipes.serializers import ReviewSerializer


# Create your views here.
class allrecipes(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        r=Recipe.objects.all()
        rec=RecipeSerializer(r,many=True)
        return Response (rec.data,status=status.HTTP_200_OK)

    def post(self,request,format=None):
        r=RecipeSerializer(data=request.data)
        if r.is_valid():
            r.save()
            return Response(r.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
class Recipedetail(APIView):
    permission_classes = [IsAuthenticated, ]
    def get_object(self,request,pk):
        try:

            return Recipe.objects.get(pk=pk)
        except:
            raise Http404

    def get(self,request,pk):
        recipe=self.get_object(request,pk)
        r= RecipeSerializer(recipe,many=True)
        return Response(r.data,status=status.HTTP_200_OK)
    def put(self, request, pk):
        recipe= self.get_object(request, pk)
        r = RecipeSerializer(recipe,data=request.data)
        if(r.is_valid()):
            r.save()
            return Response(r.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        recipe= self.get_object(request, pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class commoningredient(APIView):
    def get(self,request):

        query=self.request.query_params.get('commoningredient')
        if (query):
            recipe=Recipe.objects.filter(Recipe_ingredients__icontains=query)

            r=RecipeSerializer(recipe,many=True)
            return Response(r.data,status=status.HTTP_200_OK)

class samecuisine(APIView):
    def get(self, request):
        query = self.request.query_params.get('samecuisine')
        if (query):
            recipe = Recipe.objects.filter(cuisine__icontains=query)

            r = RecipeSerializer(recipe, many=True)
            return Response(r.data, status=status.HTTP_200_OK)
class samemealtype(APIView):
    def get(self, request):
        query = self.request.query_params.get('samemealtype')
        if (query):
            recipe = Recipe.objects.filter(meal_type__icontains=query)

            r = RecipeSerializer(recipe, many=True)
            return Response(r.data, status=status.HTTP_200_OK)

class search(APIView):
    def get(self,request):

        query=self.request.query_params.get('search')
        if (query):
            recipe=Recipe.objects.filter(Q(Recipe_name__icontains=query) | Q(Recipe_ingredients__icontains=query)| Q(Recipe_instructions__icontains=query))

            r=RecipeSerializer(recipe,many=True)
            return Response(r.data)


class CreateUser(APIView):
    def get(self,request):
        u=User.objects.all()
        us=UserSerializer(u, many=True)
        return Response(us.data,status=status.HTTP_200_OK)

    def post(self,request):
        u=UserSerializer(data=request.data)
        if(u.is_valid()):
            u.save()
            return Response(u.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
class user_logout(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        self.request.user.auth_token.delete()
        return Response (status=status.HTTP_200_OK)
class allreview(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        r=Review.objects.all()
        re=ReviewSerializer(r,many=True)
        return Response (re.data,status=status.HTTP_200_OK)


    def post(self,request,format=None):
        r=ReviewSerializer(data=request.data)
        if r.is_valid():
            r.save()
            return Response(r.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
class Reviewdetail(APIView):
    permission_classes = [IsAuthenticated, ]
    def get_object(self,request,pk):
        try:

            return Review.objects.get(pk=pk)
        except:
            raise Http404

    def get(self,request,pk):
        review=self.get_object(request,pk)
        r= ReviewSerializer(review)
        return Response(r.data,status=status.HTTP_200_OK)


    def put(self, request, pk):
        review= self.get_object(request, pk)
        r = ReviewSerializer(review,data=request.data)
        if(r.is_valid()):
            r.save()
            return Response(r.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        review= self.get_object(request, pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

