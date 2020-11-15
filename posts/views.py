from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer
from .serializers import PostSerializer
from rest_framework.exceptions import ValidationError



# Funtionality to list out all the posts in the models database
#class Postlist(generics.ListAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer

#Funtionality to list and create posts(ie POST posts)
class Postlist(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Set who has permission to call the API
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        # Make poster = to whatever user made the request
        serializer.save(poster=self.request.user)


#Funtionality to delete posts
class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Set who has permission to call the API
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objets.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You can not delete this post')









class VoteMake(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    # Need authentication to be able to read posts
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])  #get the primary key
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post')
        # Make poster = to whatever user made the request
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))


    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post')
