import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/hooks/useAuth';
import { useToast } from '@/hooks/use-toast';
import Sidebar from '@/components/Layout/Sidebar';
import Header from '@/components/Layout/Header';
import TaskCard from '@/components/TaskQueue/TaskCard';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Task } from '@/types/task';
import { apiRequest } from '@/lib/queryClient';
import { isUnauthorizedError } from '@/lib/authUtils';
import { RefreshCw, Filter } from 'lucide-react';

type TaskStatus = 'all' | 'pending' | 'processing' | 'completed' | 'failed';

export default function TaskQueue() {
  const { isAuthenticated, isLoading } = useAuth();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<TaskStatus>('all');

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      toast({
        title: 'Unauthorized',
        description: 'You are logged out. Logging in again...',
        variant: 'destructive',
      });
      setTimeout(() => {
        window.location.href = '/api/login';
      }, 500);
      return;
    }
  }, [isAuthenticated, isLoading, toast]);

  const {
    data: tasks,
    isLoading: tasksLoading,
    error: tasksError,
  } = useQuery<Task[]>({
    queryKey: ['/api/tasks'],
    enabled: isAuthenticated,
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  const updateTaskMutation = useMutation({
    mutationFn: async ({
      taskId,
      status,
    }: {
      taskId: number;
      status: string;
    }) => {
      await apiRequest('PUT', `/api/tasks/${taskId}`, { status });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/tasks'] });
      toast({
        title: 'Success',
        description: 'Task status updated successfully',
      });
    },
    onError: (error) => {
      if (isUnauthorizedError(error)) {
        toast({
          title: 'Unauthorized',
          description: 'You are logged out. Logging in again...',
          variant: 'destructive',
        });
        setTimeout(() => {
          window.location.href = '/api/login';
        }, 500);
        return;
      }

      toast({
        title: 'Error',
        description: error.message || 'Failed to update task status',
        variant: 'destructive',
      });
    },
  });

  const handleStatusChange = (taskId: number, status: string) => {
    updateTaskMutation.mutate({ taskId, status });
  };

  const handleRefresh = () => {
    queryClient.invalidateQueries({ queryKey: ['/api/tasks'] });
  };

  const filteredTasks =
    tasks?.filter((task) => activeTab === 'all' || task.status === activeTab) ||
    [];

  const getTaskCountByStatus = (status: TaskStatus) => {
    if (status === 'all') return tasks?.length || 0;
    return tasks?.filter((task) => task.status === status).length || 0;
  };

  if (isLoading) {
    return (
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">
              Loading task queue...
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header
          title="Task Queue"
          description="Monitor and manage all agent tasks and workflows"
        />

        <main className="flex-1 overflow-auto p-8">
          <div className="max-w-7xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Task Management
                  </h3>
                  <div className="flex items-center space-x-3">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleRefresh}
                      disabled={tasksLoading}
                    >
                      <RefreshCw
                        className={`w-4 h-4 mr-2 ${tasksLoading ? 'animate-spin' : ''}`}
                      />
                      Refresh
                    </Button>
                    <Button variant="outline" size="sm">
                      <Filter className="w-4 h-4 mr-2" />
                      Filter
                    </Button>
                  </div>
                </div>
              </div>

              <div className="p-6">
                <Tabs
                  value={activeTab}
                  onValueChange={(value) => setActiveTab(value as TaskStatus)}
                >
                  <TabsList className="grid w-full grid-cols-5 gap-1 p-1">
                    <TabsTrigger
                      value="all"
                      className="relative flex flex-col items-center justify-center min-h-[3rem] px-2"
                    >
                      <span className="text-xs font-medium">All Tasks</span>
                      <span className="bg-gray-100 dark:bg-gray-700 text-xs px-1.5 py-0.5 rounded-full mt-1">
                        {getTaskCountByStatus('all')}
                      </span>
                    </TabsTrigger>
                    <TabsTrigger
                      value="pending"
                      className="relative flex flex-col items-center justify-center min-h-[3rem] px-2"
                    >
                      <span className="text-xs font-medium">Pending</span>
                      <span className="bg-warning/10 text-warning text-xs px-1.5 py-0.5 rounded-full mt-1">
                        {getTaskCountByStatus('pending')}
                      </span>
                    </TabsTrigger>
                    <TabsTrigger
                      value="processing"
                      className="relative flex flex-col items-center justify-center min-h-[3rem] px-2"
                    >
                      <span className="text-xs font-medium">Processing</span>
                      <span className="bg-blue-100 text-blue-600 text-xs px-1.5 py-0.5 rounded-full mt-1">
                        {getTaskCountByStatus('processing')}
                      </span>
                    </TabsTrigger>
                    <TabsTrigger
                      value="completed"
                      className="relative flex flex-col items-center justify-center min-h-[3rem] px-2"
                    >
                      <span className="text-xs font-medium">Completed</span>
                      <span className="bg-success/10 text-success text-xs px-1.5 py-0.5 rounded-full mt-1">
                        {getTaskCountByStatus('completed')}
                      </span>
                    </TabsTrigger>
                    <TabsTrigger
                      value="failed"
                      className="relative flex flex-col items-center justify-center min-h-[3rem] px-2"
                    >
                      <span className="text-xs font-medium">Failed</span>
                      <span className="bg-error/10 text-error text-xs px-1.5 py-0.5 rounded-full mt-1">
                        {getTaskCountByStatus('failed')}
                      </span>
                    </TabsTrigger>
                  </TabsList>

                  <div className="mt-6">
                    <TabsContent value={activeTab} className="mt-0">
                      {tasksLoading ? (
                        <div className="space-y-4">
                          {[...Array(5)].map((_, i) => (
                            <Card key={i}>
                              <CardContent className="p-6">
                                <div className="flex items-start justify-between">
                                  <div className="flex-1 space-y-3">
                                    <div className="flex items-center space-x-3">
                                      <Skeleton className="h-6 w-48" />
                                      <Skeleton className="h-5 w-16" />
                                      <Skeleton className="h-5 w-12" />
                                    </div>
                                    <Skeleton className="h-4 w-96" />
                                    <div className="flex space-x-4">
                                      <Skeleton className="h-3 w-20" />
                                      <Skeleton className="h-3 w-24" />
                                    </div>
                                  </div>
                                  <div className="flex space-x-2">
                                    <Skeleton className="h-8 w-16" />
                                    <Skeleton className="h-8 w-8" />
                                  </div>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      ) : tasksError ? (
                        <div className="text-center py-8">
                          <p className="text-error mb-4">
                            Failed to load tasks
                          </p>
                          <Button variant="outline" onClick={handleRefresh}>
                            Retry
                          </Button>
                        </div>
                      ) : filteredTasks.length === 0 ? (
                        <div className="text-center py-12">
                          <p className="text-gray-500 dark:text-gray-400 text-lg mb-2">
                            No {activeTab === 'all' ? '' : activeTab} tasks
                            found
                          </p>
                          <p className="text-sm text-gray-400 dark:text-gray-500">
                            Tasks will appear here as agents complete their work
                          </p>
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {filteredTasks.map((task) => (
                            <TaskCard
                              key={task.id}
                              task={task}
                              onStatusChange={handleStatusChange}
                            />
                          ))}
                        </div>
                      )}
                    </TabsContent>
                  </div>
                </Tabs>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
