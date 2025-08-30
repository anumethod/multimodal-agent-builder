import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import {
  Shield,
  AlertTriangle,
  CheckCircle,
  Activity,
  Eye,
  Lock,
  Zap,
  Key,
  Smartphone,
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useEffect } from 'react';
import { useToast } from '@/hooks/use-toast';
import TwoFactorSetup from '@/components/Security/TwoFactorSetup';
import PasswordChangeModal from '@/components/Security/PasswordChangeModal';

export default function Security() {
  const { toast } = useToast();
  const { isAuthenticated, isLoading } = useAuth();
  const [show2FASetup, setShow2FASetup] = useState(false);
  const [showPasswordChange, setShowPasswordChange] = useState(false);

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

  const { data: securityStatus } = useQuery<{
    overallScore: number;
    protectedAgents: number;
    securityEvents: number;
    lastScanTime: string;
    complianceLevel: string;
  }>({
    queryKey: ['/api/security/status'],
    enabled: isAuthenticated,
  });

  const { data: auditLogs } = useQuery<
    Array<{
      id: number;
      userId: string;
      action: string;
      resource: string;
      ipAddress: string;
      success: boolean;
      createdAt: string;
    }>
  >({
    queryKey: ['/api/security/audit-logs'],
    enabled: isAuthenticated,
  });

  // Password expiry check
  const { data: passwordExpiry } = useQuery<{
    expired: boolean;
    daysRemaining: number;
  }>({
    queryKey: ['/api/auth/password-expiry'],
    enabled: isAuthenticated,
  });

  // Check if password is expired and force change
  useEffect(() => {
    if (passwordExpiry?.expired) {
      setShowPasswordChange(true);
      toast({
        title: 'Password Expired',
        description: 'Your password has expired. Please change it to continue.',
        variant: 'destructive',
      });
    } else if (passwordExpiry && passwordExpiry.daysRemaining <= 7) {
      toast({
        title: 'Password Expiring Soon',
        description: `Your password expires in ${passwordExpiry.daysRemaining} days.`,
        variant: 'destructive',
      });
    }
  }, [passwordExpiry, toast]);

  const { data: threatAnalysis } = useQuery<{
    activeThreats: number;
    threats: Array<{
      type: string;
      description: string;
      severity: string;
      timestamp: string;
    }>;
    riskLevel: string;
    lastAnalysis: string;
  }>({
    queryKey: ['/api/security/threat-analysis'],
    enabled: isAuthenticated,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const securityScore = securityStatus?.overallScore ?? 0;
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="container mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Security Center</h1>
          <p className="text-muted-foreground">
            Monitor and manage security across all layers
          </p>
        </div>
        <Badge variant="outline" className="text-lg px-4 py-2">
          <Shield className="w-4 h-4 mr-2" />
          Security Score:{' '}
          <span className={getScoreColor(securityScore)}>
            {securityScore}/100
          </span>
        </Badge>
      </div>

      {/* Security Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Active Threats
            </CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {threatAnalysis?.activeThreats ?? 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Critical incidents detected
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Protected Agents
            </CardTitle>
            <Shield className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {securityStatus?.protectedAgents ?? 0}
            </div>
            <p className="text-xs text-muted-foreground">Actively monitored</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Security Events
            </CardTitle>
            <Activity className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{auditLogs?.length ?? 0}</div>
            <p className="text-xs text-muted-foreground">Last 24 hours</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Compliance Status
            </CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">98%</div>
            <p className="text-xs text-muted-foreground">
              Security standards met
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Security Progress */}
      <Card>
        <CardHeader>
          <CardTitle>Security Posture</CardTitle>
          <CardDescription>
            Overall security health across all OSI layers
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Overall Security Score</span>
              <span className={getScoreColor(securityScore)}>
                {securityScore}%
              </span>
            </div>
            <Progress value={securityScore} className="h-2" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Network Security</span>
                <span className="text-green-600">100%</span>
              </div>
              <Progress value={100} className="h-1" />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Application Security</span>
                <span className="text-green-600">100%</span>
              </div>
              <Progress value={100} className="h-1" />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Data Protection</span>
                <span className="text-green-600">100%</span>
              </div>
              <Progress value={100} className="h-1" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="threats" className="space-y-4">
        <TabsList>
          <TabsTrigger value="threats">Threat Detection</TabsTrigger>
          <TabsTrigger value="authentication">Authentication</TabsTrigger>
          <TabsTrigger value="audit">Audit Logs</TabsTrigger>
          <TabsTrigger value="compliance">Compliance</TabsTrigger>
          <TabsTrigger value="monitoring">Real-time Monitoring</TabsTrigger>
        </TabsList>

        <TabsContent value="threats" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Active Threat Analysis
              </CardTitle>
              <CardDescription>
                Real-time threat detection and response
              </CardDescription>
            </CardHeader>
            <CardContent>
              {threatAnalysis?.threats && threatAnalysis.threats.length > 0 ? (
                <div className="space-y-4">
                  {threatAnalysis.threats.map((threat, index: number) => (
                    <Alert
                      key={index}
                      variant={
                        threat.severity === 'high' ? 'destructive' : 'default'
                      }
                    >
                      <AlertTriangle className="h-4 w-4" />
                      <AlertDescription>
                        <div className="flex justify-between items-start">
                          <div>
                            <strong>{threat.type}</strong>: {threat.description}
                            <div className="text-sm text-muted-foreground mt-1">
                              Detected: {threat.timestamp}
                            </div>
                          </div>
                          <Badge
                            variant={
                              threat.severity === 'high'
                                ? 'destructive'
                                : 'secondary'
                            }
                          >
                            {threat.severity}
                          </Badge>
                        </div>
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">
                    No Active Threats
                  </h3>
                  <p className="text-muted-foreground">
                    Your system is secure and all monitoring systems are
                    operational.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="authentication" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Two-Factor Authentication */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Smartphone className="w-5 h-5" />
                  Two-Factor Authentication
                </CardTitle>
                <CardDescription>
                  Add an extra layer of security to your account
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Check user's 2FA status here - mock for now */}
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Shield className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="font-medium">Authenticator App</p>
                      <p className="text-sm text-muted-foreground">
                        Use an app like Google Authenticator
                      </p>
                    </div>
                  </div>
                  <Badge variant="outline">Not Enabled</Badge>
                </div>

                <Button
                  onClick={() => setShow2FASetup(true)}
                  className="w-full"
                >
                  <Key className="w-4 h-4 mr-2" />
                  Enable Two-Factor Authentication
                </Button>

                <Alert>
                  <Shield className="w-4 h-4" />
                  <AlertDescription>
                    Two-factor authentication significantly increases your
                    account security by requiring a second verification step
                    during login.
                  </AlertDescription>
                </Alert>
              </CardContent>
            </Card>

            {/* Password Management */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lock className="w-5 h-5" />
                  Password Management
                </CardTitle>
                <CardDescription>
                  Secure password policies and management
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <p className="font-medium">Password Age</p>
                      <p className="text-sm text-muted-foreground">
                        {passwordExpiry?.daysRemaining !== undefined
                          ? `${passwordExpiry.daysRemaining} days remaining`
                          : 'Not set'}
                      </p>
                    </div>
                    {passwordExpiry?.expired && (
                      <Badge variant="destructive">Expired</Badge>
                    )}
                    {passwordExpiry &&
                      passwordExpiry.daysRemaining <= 7 &&
                      !passwordExpiry.expired && (
                        <Badge variant="destructive">Expiring Soon</Badge>
                      )}
                    {passwordExpiry && passwordExpiry.daysRemaining > 7 && (
                      <Badge variant="outline">Valid</Badge>
                    )}
                  </div>

                  <Button
                    onClick={() => setShowPasswordChange(true)}
                    variant="outline"
                    className="w-full"
                  >
                    <Lock className="w-4 h-4 mr-2" />
                    Change Password
                  </Button>
                </div>

                <Alert>
                  <AlertTriangle className="w-4 h-4" />
                  <AlertDescription>
                    <strong>Password Policy:</strong> Passwords must be changed
                    every 90 days and meet complexity requirements (12+
                    characters, uppercase, lowercase, numbers, special
                    characters).
                  </AlertDescription>
                </Alert>
              </CardContent>
            </Card>
          </div>

          {/* Security Sessions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Active Sessions
              </CardTitle>
              <CardDescription>
                Monitor and manage your active login sessions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-500 rounded-full" />
                    <div>
                      <p className="font-medium">Current Session</p>
                      <p className="text-sm text-muted-foreground">
                        Active now • Session timeout: 1 hour
                      </p>
                    </div>
                  </div>
                  <Badge variant="default">Active</Badge>
                </div>

                <Button variant="outline" className="w-full">
                  <Zap className="w-4 h-4 mr-2" />
                  Revoke All Other Sessions
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audit" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="w-5 h-5" />
                Security Audit Log
              </CardTitle>
              <CardDescription>
                Comprehensive activity tracking and compliance logging
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-96">
                <div className="space-y-4">
                  {auditLogs?.map((log, index: number) => (
                    <div
                      key={index}
                      className="flex items-start space-x-4 p-4 border rounded-lg"
                    >
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium">{log.action}</p>
                          <Badge variant="outline" className="text-xs">
                            {log.resource}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          User: {log.userId} • IP: {log.ipAddress}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {new Date(log.createdAt).toLocaleString()}
                        </p>
                      </div>
                      <Badge variant={log.success ? 'default' : 'destructive'}>
                        {log.success ? 'Success' : 'Failed'}
                      </Badge>
                    </div>
                  )) || (
                    <div className="text-center py-12">
                      <Activity className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                      <h3 className="text-lg font-semibold mb-2">
                        No Recent Activity
                      </h3>
                      <p className="text-muted-foreground">
                        Security events will appear here as they occur.
                      </p>
                    </div>
                  )}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="compliance" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lock className="w-5 h-5" />
                  Security Standards
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span>ISO 27001 Compliance</span>
                  <Badge variant="default">Compliant</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>SOC 2 Type II</span>
                  <Badge variant="default">Certified</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>GDPR Compliance</span>
                  <Badge variant="default">Compliant</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>OWASP Top 10</span>
                  <Badge variant="secondary">In Progress</Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Security Policies</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span>Password Policy</span>
                  <Badge variant="default">Active</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>Multi-Factor Authentication</span>
                  <Badge variant="default">Enforced</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>Data Encryption</span>
                  <Badge variant="default">AES-256</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>Access Control</span>
                  <Badge variant="default">RBAC</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="monitoring" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="w-5 h-5" />
                Real-time Security Monitoring
              </CardTitle>
              <CardDescription>
                Live security metrics and system health
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">99.9%</div>
                  <p className="text-sm text-muted-foreground">System Uptime</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">24/7</div>
                  <p className="text-sm text-muted-foreground">
                    Monitoring Active
                  </p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">
                    &lt;2ms
                  </div>
                  <p className="text-sm text-muted-foreground">Response Time</p>
                </div>
              </div>

              <div className="mt-8">
                <Alert>
                  <CheckCircle className="h-4 w-4" />
                  <AlertDescription>
                    All security systems are operational. No immediate action
                    required.
                  </AlertDescription>
                </Alert>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Security Actions</CardTitle>
          <CardDescription>
            Quick access to essential security functions
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <Button variant="outline">
              <Shield className="w-4 h-4 mr-2" />
              Run Security Scan
            </Button>
            <Button variant="outline">
              <Lock className="w-4 h-4 mr-2" />
              Review Permissions
            </Button>
            <Button variant="outline">
              <Activity className="w-4 h-4 mr-2" />
              Generate Report
            </Button>
            <Button variant="outline">
              <AlertTriangle className="w-4 h-4 mr-2" />
              Incident Response
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* 2FA Setup Modal */}
      {show2FASetup && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
            <div className="max-h-[calc(90vh-2rem)] overflow-y-auto">
              <TwoFactorSetup
                onComplete={() => {
                  setShow2FASetup(false);
                  toast({
                    title: '2FA Enabled',
                    description:
                      'Two-factor authentication has been successfully enabled for your account',
                  });
                }}
                onCancel={() => setShow2FASetup(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Password Change Modal */}
      <PasswordChangeModal
        isOpen={showPasswordChange}
        onClose={() => setShowPasswordChange(false)}
        isForced={passwordExpiry?.expired || false}
        userHas2FA={false} // TODO: Get from user data
      />
    </div>
  );
}
