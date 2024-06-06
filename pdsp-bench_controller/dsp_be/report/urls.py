from django.urls import path

from . import views



urlpatterns = [
    path('getAll/<str:user_id>', views.GetAllJobs.as_view(), name='Get all jobs'),
    path('getThisClusterJobs/<str:cluster_id>', views.GetThisClusterJobs.as_view(), name = 'Get this cluster jobs'),
    path('stopJob/<str:cluster_id>/<str:job_id>', views.StopJob.as_view(), name='Stop a job'),
    path('getJobInfo/<str:cluster_id>/<str:job_id>', views.GetJobInfo.as_view(), name='Get info of a job'),
    path('getOperatorInfo/<str:cluster_id>/<str:job_id>', views.GetOperatorInfo.as_view(), name='Get info of job operators'),
    path('getJobMetrics/<str:cluster_id>/<str:job_id>', views.GetJobMetrics.as_view(), name='Get job metrics'),
    path('getHistoricalMetrics/<str:cluster_id>/<str:job_id>', views.GetHistoricalMetrics.as_view(), name='Get historical metrics'),
    path('getIndividualGraphData',views.GetIndividualGraphData.as_view(), name='Get Individual GraphData'),
    path('getCompareGraphData',views.GetCompareGraphData.as_view(), name='Get Compare GraphData'),
    path('getSinkTopicResults/<str:cluster_id>/<str:job_id>/<str:data_size>',views.GetSinkTopicResults.as_view(), name='Get Sink Topic Results'),
]
