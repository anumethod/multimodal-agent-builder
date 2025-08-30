import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Shield, Bot, Zap, Users } from 'lucide-react';

export default function Landing() {
  const handleLogin = () => {
    window.location.href = '/api/login';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-3 mb-6">
            <div className="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center">
              <Bot className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
                Agent Factory
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                Neurodivergence Framework
              </p>
            </div>
          </div>

          <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
            Secure AI Agent Platform for Business Automation
          </h2>

          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8">
            Create, manage, and deploy specialized AI agents for every aspect of
            your business operations. Built with security-first principles and
            designed for neurodivergent-friendly workflows.
          </p>

          <Button
            onClick={handleLogin}
            size="lg"
            className="bg-primary hover:bg-blue-700 text-white px-8 py-4 text-lg font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
          >
            Get Started
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          <Card className="text-center">
            <CardHeader>
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Bot className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <CardTitle>AI Agents</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Create specialized agents for social media, email marketing,
                analytics, and more
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Shield className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <CardTitle>Security First</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Enterprise-grade security with encryption, audit logging, and
                access controls
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Zap className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <CardTitle>Automation</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Automate repetitive tasks with intelligent workflows and
                approval systems
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Users className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <CardTitle>Neurodivergent</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Designed with clear interfaces and structured workflows for
                accessibility
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-16">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
            Comprehensive Agent Types
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-sm font-semibold text-purple-600 dark:text-purple-400">
                  SM
                </span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  Social Media Agents
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Content generation, scheduling, and engagement analysis
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">
                  EM
                </span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  Email Marketing
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Campaign creation, automation, and performance tracking
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-sm font-semibold text-green-600 dark:text-green-400">
                  AN
                </span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  Analytics & BI
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Data analysis, reporting, and business intelligence
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-sm font-semibold text-orange-600 dark:text-orange-400">
                  FS
                </span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  File System
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Organization, backup, and monitoring
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
                  DN
                </span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  DNS Management
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Domain configuration and propagation monitoring
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-pink-100 dark:bg-pink-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-sm font-semibold text-pink-600 dark:text-pink-400">
                  TR
                </span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  Traffic Monitoring
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Real-time traffic analysis and alerting
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="text-center">
          <div className="inline-flex items-center space-x-2 bg-secure/10 text-secure px-4 py-2 rounded-lg mb-4">
            <Shield className="w-4 h-4" />
            <span className="text-sm font-medium">
              Enterprise Security Standards
            </span>
          </div>

          <p className="text-gray-600 dark:text-gray-400 mb-8">
            Built with enterprise-grade security features including end-to-end
            encryption, comprehensive audit logging, and role-based access
            controls.
          </p>

          <Button
            onClick={handleLogin}
            variant="outline"
            size="lg"
            className="border-primary text-primary hover:bg-primary hover:text-white"
          >
            Start Building Agents
          </Button>
        </div>
      </div>
    </div>
  );
}
