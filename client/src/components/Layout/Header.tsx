import { Button } from '@/components/ui/button';
import { useWebSocket } from '@/hooks/useWebSocket';
import { cn } from '@/lib/utils';
import { Shield, Plus } from 'lucide-react';

interface HeaderProps {
  title: string;
  description?: string;
  onCreateAgent?: () => void;
}

export default function Header({
  title,
  description,
  onCreateAgent,
}: HeaderProps) {
  const { connectionStatus } = useWebSocket();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 px-8 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            {title}
          </h2>
          {description && (
            <p className="text-gray-600 dark:text-gray-300 mt-1">
              {description}
            </p>
          )}
        </div>
        <div className="flex items-center space-x-4">
          <div
            className={cn(
              'flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium',
              connectionStatus === 'connected'
                ? 'bg-secure/10 text-secure'
                : 'bg-error/10 text-error',
            )}
          >
            <Shield className="text-sm w-4 h-4" />
            <span>
              {connectionStatus === 'connected'
                ? 'System Secure'
                : 'Connection Lost'}
            </span>
          </div>
          {onCreateAgent && (
            <Button
              onClick={onCreateAgent}
              className="bg-primary text-white hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <Plus className="text-sm w-4 h-4" />
              <span>Create Agent</span>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
}
