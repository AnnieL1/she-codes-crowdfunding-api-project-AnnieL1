from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Project, Pledge
from .serializers import ProjectSerializer, ProjectDetailSerializer, PledgeSerializer
from django.http import Http404
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(   #better to put a catch all return after the if statement, rather than using a else statement, just in case if statement is really long and complicated. Don't want to make it hard to read because people will miss it.
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly        
    ]

    def get_object(self, pk):
        try: #tells python what to do and will show the return statement if it works
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist: #native python language that gets released into the interpreter when something goes wrong
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)  # changed to ProjectSerializer from ProjectDetailSerializer. Why does it still work?
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance = project,
            data = data,
            partial = True 
        )
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)



class PledgeList(generics.ListCreateAPIView):  #see Meta from serializer.py
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)
    
    ## all the code below this line and blocked out gets deleted because we have used the Meta method in serialize.py
    # def get(self, request):
    #     pledges = Pledge.objects.all()
    #     serializer = PledgeSerializer(pledges, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = PledgeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )