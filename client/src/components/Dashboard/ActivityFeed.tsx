import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Activity } from '@/types/task';
import { CheckCircle, Clock, Cog, Mail } from 'lucide-react';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';

function getActivityIcon(type: string) {
  switch (type) {
    case 'agent.created':
    case 'agent.updated':
    case 'agent.initialized':
      return { icon: Cog, color: 'bg-primary/10 text-primary' };
    case 'task.completed':
    case 'approval.approved':
      return { icon: CheckCircle, color: 'bg-success/10 text-success' };
    case 'task.pending':
    case 'approval.pending':
      return { icon: Clock, color: 'bg-warning/10 text-warning' };
    case 'email.sent':
      return { icon: Mail, color: 'bg-purple-100 text-purple-600' };
    default:
      return { icon: Cog, color: 'bg-gray-100 text-gray-600' };
  }
}

export default function ActivityFeed() {
  const {
    data: activities,
    isLoading,
    error,
  } = useQuery<Activity[]>({
    queryKey: ['/api/dashboard/activities'],
    refetchInterval: 120000, // Refresh every 2 minutes to reduce API load
    refetchOnWindowFocus: false, // Prevent refetch on window focus
    refetchOnMount: true,
  });

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="flex items-start space-x-3">
                <Skeleton className="w-8 h-8 rounded-full" />
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-3 w-1/4" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-error text-center py-4">
            Failed to load activity feed
          </p>
        </CardContent>
      </Card>
    );
  }

  if (!activities || activities.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 dark:text-gray-400 text-center py-4">
            No recent activity to display
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => {
            const { icon: Icon, color } = getActivityIcon(activity.type);

            return (
              <div key={activity.id} className="flex items-start space-x-3">
                <div
                  className={cn(
                    'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                    color,
                  )}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 dark:text-white">
                    {activity.message}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {activity.createdAt
                      ? formatDistanceToNow(new Date(activity.createdAt), {
                          addSuffix: true,
                        })
                      : 'Just now'}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
