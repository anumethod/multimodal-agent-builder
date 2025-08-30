import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Shield, Check, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SecurityCheck {
  name: string;
  status: 'secure' | 'warning' | 'error';
  description: string;
}

export default function SecurityStatus() {
  const { connectionStatus } = useWebSocket();

  const securityChecks: SecurityCheck[] = [
    {
      name: 'API Keys Encrypted',
      status: 'secure',
      description: 'All API keys are encrypted at rest',
    },
    {
      name: 'Rate Limiting Active',
      status: 'secure',
      description: 'Request rate limiting is enabled',
    },
    {
      name: 'Audit Logging Enabled',
      status: 'secure',
      description: 'All actions are being logged',
    },
    {
      name: '2FA Pending',
      status: 'warning',
      description: 'Two-factor authentication setup recommended',
    },
  ];

  const overallStatus = securityChecks.every(
    (check) => check.status === 'secure',
  )
    ? 'secure'
    : securityChecks.some((check) => check.status === 'error')
      ? 'error'
      : 'warning';

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Security Status</CardTitle>
          <div
            className={cn(
              'flex items-center space-x-2 text-sm font-medium',
              overallStatus === 'secure'
                ? 'text-secure'
                : overallStatus === 'warning'
                  ? 'text-warning'
                  : 'text-error',
            )}
          >
            <Shield className="w-4 h-4" />
            <span>
              {overallStatus === 'secure'
                ? 'Secure'
                : overallStatus === 'warning'
                  ? 'Warning'
                  : 'At Risk'}
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {securityChecks.map((check) => (
          <div key={check.name} className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div
                className={cn(
                  'w-2 h-2 rounded-full',
                  check.status === 'secure'
                    ? 'bg-secure'
                    : check.status === 'warning'
                      ? 'bg-warning'
                      : 'bg-error',
                )}
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">
                {check.name}
              </span>
            </div>
            {check.status === 'secure' ? (
              <Check className="w-4 h-4 text-secure" />
            ) : (
              <AlertTriangle
                className={cn(
                  'w-4 h-4',
                  check.status === 'warning' ? 'text-warning' : 'text-error',
                )}
              />
            )}
          </div>
        ))}

        <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-500 dark:text-gray-400">
              Connection Status
            </span>
            <span
              className={cn(
                'font-medium',
                connectionStatus === 'connected'
                  ? 'text-secure'
                  : connectionStatus === 'connecting'
                    ? 'text-warning'
                    : 'text-error',
              )}
            >
              {connectionStatus === 'connected'
                ? 'Connected'
                : connectionStatus === 'connecting'
                  ? 'Connecting...'
                  : 'Disconnected'}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
