import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useToast } from '@/hooks/use-toast';
import Sidebar from '@/components/Layout/Sidebar';
import Header from '@/components/Layout/Header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { User, Shield, Bell, Palette, Database } from 'lucide-react';

export default function Settings() {
  const { isAuthenticated, isLoading } = useAuth();
  const { toast } = useToast();
  const [settings, setSettings] = useState({
    profile: {
      name: 'Agent Administrator',
      email: 'admin@agentfactory.com',
      role: 'System Administrator',
    },
    security: {
      twoFactorAuth: true,
      sessionTimeout: 30,
      securityAlerts: true,
    },
    notifications: {
      emailNotifications: true,
      pushNotifications: false,
      securityAlerts: true,
      taskUpdates: true,
    },
    appearance: {
      theme: 'system',
      language: 'en',
      timezone: 'UTC',
    },
    system: {
      autoBackup: true,
      debugMode: false,
      performanceMonitoring: true,
    },
  });

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

  const handleSaveSettings = () => {
    toast({
      title: 'Settings Saved',
      description: 'Your settings have been updated successfully',
    });
  };

  const handleResetSettings = () => {
    toast({
      title: 'Settings Reset',
      description: 'Settings have been reset to defaults',
    });
  };

  if (isLoading) {
    return (
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">
              Loading settings...
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
          title="Settings"
          description="Configure your agent factory platform settings"
        />

        <main className="flex-1 overflow-auto p-8">
          <div className="max-w-4xl mx-auto">
            <Tabs defaultValue="profile" className="space-y-6">
              <TabsList className="grid w-full grid-cols-5 gap-1 p-1">
                <TabsTrigger
                  value="profile"
                  className="flex flex-col items-center justify-center min-h-[3rem] px-2"
                >
                  <User className="w-4 h-4" />
                  <span className="text-xs font-medium mt-1">Profile</span>
                </TabsTrigger>
                <TabsTrigger
                  value="security"
                  className="flex flex-col items-center justify-center min-h-[3rem] px-2"
                >
                  <Shield className="w-4 h-4" />
                  <span className="text-xs font-medium mt-1">Security</span>
                </TabsTrigger>
                <TabsTrigger
                  value="notifications"
                  className="flex flex-col items-center justify-center min-h-[3rem] px-2"
                >
                  <Bell className="w-4 h-4" />
                  <span className="text-xs font-medium mt-1">
                    Notifications
                  </span>
                </TabsTrigger>
                <TabsTrigger
                  value="appearance"
                  className="flex flex-col items-center justify-center min-h-[3rem] px-2"
                >
                  <Palette className="w-4 h-4" />
                  <span className="text-xs font-medium mt-1">Appearance</span>
                </TabsTrigger>
                <TabsTrigger
                  value="system"
                  className="flex flex-col items-center justify-center min-h-[3rem] px-2"
                >
                  <Database className="w-4 h-4" />
                  <span className="text-xs font-medium mt-1">System</span>
                </TabsTrigger>
              </TabsList>

              <TabsContent value="profile" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Profile Information</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Full Name</Label>
                      <Input
                        id="name"
                        value={settings.profile.name}
                        onChange={(e) =>
                          setSettings({
                            ...settings,
                            profile: {
                              ...settings.profile,
                              name: e.target.value,
                            },
                          })
                        }
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email Address</Label>
                      <Input
                        id="email"
                        type="email"
                        value={settings.profile.email}
                        onChange={(e) =>
                          setSettings({
                            ...settings,
                            profile: {
                              ...settings.profile,
                              email: e.target.value,
                            },
                          })
                        }
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="role">Role</Label>
                      <Input id="role" value={settings.profile.role} disabled />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="security" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Security Settings</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Two-Factor Authentication</Label>
                        <p className="text-sm text-muted-foreground">
                          Add an extra layer of security to your account
                        </p>
                      </div>
                      <Switch
                        checked={settings.security.twoFactorAuth}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            security: {
                              ...settings.security,
                              twoFactorAuth: checked,
                            },
                          })
                        }
                      />
                    </div>
                    <Separator />
                    <div className="space-y-2">
                      <Label>Session Timeout (minutes)</Label>
                      <Select
                        value={settings.security.sessionTimeout.toString()}
                        onValueChange={(value) =>
                          setSettings({
                            ...settings,
                            security: {
                              ...settings.security,
                              sessionTimeout: parseInt(value),
                            },
                          })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="15">15 minutes</SelectItem>
                          <SelectItem value="30">30 minutes</SelectItem>
                          <SelectItem value="60">1 hour</SelectItem>
                          <SelectItem value="120">2 hours</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <Separator />
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Security Alerts</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive alerts for suspicious activities
                        </p>
                      </div>
                      <Switch
                        checked={settings.security.securityAlerts}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            security: {
                              ...settings.security,
                              securityAlerts: checked,
                            },
                          })
                        }
                      />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="notifications" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Notification Preferences</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Email Notifications</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive updates via email
                        </p>
                      </div>
                      <Switch
                        checked={settings.notifications.emailNotifications}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            notifications: {
                              ...settings.notifications,
                              emailNotifications: checked,
                            },
                          })
                        }
                      />
                    </div>
                    <Separator />
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Task Updates</Label>
                        <p className="text-sm text-muted-foreground">
                          Notifications when tasks complete
                        </p>
                      </div>
                      <Switch
                        checked={settings.notifications.taskUpdates}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            notifications: {
                              ...settings.notifications,
                              taskUpdates: checked,
                            },
                          })
                        }
                      />
                    </div>
                    <Separator />
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Security Alerts</Label>
                        <p className="text-sm text-muted-foreground">
                          Critical security notifications
                        </p>
                      </div>
                      <Switch
                        checked={settings.notifications.securityAlerts}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            notifications: {
                              ...settings.notifications,
                              securityAlerts: checked,
                            },
                          })
                        }
                      />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="appearance" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Appearance Settings</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-2">
                      <Label>Theme</Label>
                      <Select
                        value={settings.appearance.theme}
                        onValueChange={(value) =>
                          setSettings({
                            ...settings,
                            appearance: {
                              ...settings.appearance,
                              theme: value,
                            },
                          })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="light">Light</SelectItem>
                          <SelectItem value="dark">Dark</SelectItem>
                          <SelectItem value="system">System</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <Separator />
                    <div className="space-y-2">
                      <Label>Language</Label>
                      <Select
                        value={settings.appearance.language}
                        onValueChange={(value) =>
                          setSettings({
                            ...settings,
                            appearance: {
                              ...settings.appearance,
                              language: value,
                            },
                          })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="en">English</SelectItem>
                          <SelectItem value="es">Spanish</SelectItem>
                          <SelectItem value="fr">French</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <Separator />
                    <div className="space-y-2">
                      <Label>Timezone</Label>
                      <Select
                        value={settings.appearance.timezone}
                        onValueChange={(value) =>
                          setSettings({
                            ...settings,
                            appearance: {
                              ...settings.appearance,
                              timezone: value,
                            },
                          })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="UTC">UTC</SelectItem>
                          <SelectItem value="EST">Eastern Time</SelectItem>
                          <SelectItem value="PST">Pacific Time</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="system" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>System Configuration</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Auto Backup</Label>
                        <p className="text-sm text-muted-foreground">
                          Automatically backup system data
                        </p>
                      </div>
                      <Switch
                        checked={settings.system.autoBackup}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            system: { ...settings.system, autoBackup: checked },
                          })
                        }
                      />
                    </div>
                    <Separator />
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Performance Monitoring</Label>
                        <p className="text-sm text-muted-foreground">
                          Monitor system performance metrics
                        </p>
                      </div>
                      <Switch
                        checked={settings.system.performanceMonitoring}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            system: {
                              ...settings.system,
                              performanceMonitoring: checked,
                            },
                          })
                        }
                      />
                    </div>
                    <Separator />
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Debug Mode</Label>
                        <p className="text-sm text-muted-foreground">
                          Enable detailed logging for troubleshooting
                        </p>
                      </div>
                      <Switch
                        checked={settings.system.debugMode}
                        onCheckedChange={(checked) =>
                          setSettings({
                            ...settings,
                            system: { ...settings.system, debugMode: checked },
                          })
                        }
                      />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>

            <div className="flex justify-end space-x-4 pt-6">
              <Button variant="outline" onClick={handleResetSettings}>
                Reset to Defaults
              </Button>
              <Button onClick={handleSaveSettings}>Save Settings</Button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
