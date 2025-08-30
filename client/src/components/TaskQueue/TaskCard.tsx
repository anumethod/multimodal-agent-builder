import { Task } from '@/types/task';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';
import {
  Clock,
  Play,
  CheckCircle,
  XCircle,
  AlertCircle,
  MoreHorizontal,
} from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onStatusChange?: (taskId: number, status: string) => void;
}

function getStatusConfig(status: string) {
  switch (status) {
    case 'pending':
      return {
        icon: Clock,
        color: 'bg-gray-100 text-gray-600',
        label: 'Pending',
      };
    case 'processing':
      return {
        icon: Play,
        color: 'bg-blue-100 text-blue-600',
        label: 'Processing',
      };
    case 'completed':
      return {
        icon: CheckCircle,
        color: 'bg-success/10 text-success',
        label: 'Completed',
      };
    case 'failed':
      return {
        icon: XCircle,
        color: 'bg-error/10 text-error',
        label: 'Failed',
      };
    case 'cancelled':
      return {
        icon: AlertCircle,
        color: 'bg-warning/10 text-warning',
        label: 'Cancelled',
      };
    default:
      return {
        icon: Clock,
        color: 'bg-gray-100 text-gray-600',
        label: status,
      };
  }
}

function getPriorityColor(priority: string) {
  switch (priority) {
    case 'high':
      return 'border-l-error';
    case 'medium':
      return 'border-l-warning';
    case 'low':
      return 'border-l-success';
    default:
      return 'border-l-gray-300';
  }
}

export default function TaskCard({ task, onStatusChange }: TaskCardProps) {
  const statusConfig = getStatusConfig(task.status);
  const StatusIcon = statusConfig.icon;

  return (
    <Card className={cn('border-l-4', getPriorityColor(task.priority))}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h3 className="font-semibold text-gray-900 dark:text-white">
                {task.title}
              </h3>
              <Badge className={cn('text-xs', statusConfig.color)}>
                <StatusIcon className="w-3 h-3 mr-1" />
                {statusConfig.label}
              </Badge>
              <Badge variant="outline" className="text-xs">
                {task.priority}
              </Badge>
            </div>

            {task.description && (
              <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
                {task.description}
              </p>
            )}

            <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
              <span>Type: {task.type}</span>
              {task.createdAt && (
                <span>
                  Created{' '}
                  {formatDistanceToNow(new Date(task.createdAt), {
                    addSuffix: true,
                  })}
                </span>
              )}
              {task.scheduledFor &&
                new Date(task.scheduledFor) > new Date() && (
                  <span>
                    Scheduled for{' '}
                    {formatDistanceToNow(new Date(task.scheduledFor), {
                      addSuffix: true,
                    })}
                  </span>
                )}
            </div>

            {task.error && (
              <div className="mt-3 p-2 bg-error/10 border border-error/20 rounded text-sm text-error">
                Error: {task.error}
              </div>
            )}

            {task.result && task.status === 'completed' && (
              <div className="mt-3 p-2 bg-success/10 border border-success/20 rounded text-sm">
                <strong>Result:</strong> {JSON.stringify(task.result, null, 2)}
              </div>
            )}
          </div>

          <div className="flex items-center space-x-2 ml-4">
            {task.status === 'pending' && onStatusChange && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => onStatusChange(task.id, 'cancelled')}
              >
                Cancel
              </Button>
            )}

            {task.status === 'failed' && onStatusChange && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => onStatusChange(task.id, 'pending')}
              >
                Retry
              </Button>
            )}

            <Button size="sm" variant="ghost">
              <MoreHorizontal className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
