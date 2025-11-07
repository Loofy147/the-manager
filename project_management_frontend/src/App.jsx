import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import RoleManagement from '@/components/RoleManagement.jsx'
import ProjectManagement from '@/components/ProjectManagement.jsx'
import FinanceManagement from '@/components/FinanceManagement.jsx'
import { 
  Users, 
  FolderOpen, 
  BarChart3, 
  Settings, 
  Plus, 
  Search,
  Bell,
  Menu,
  Home,
  UserCheck,
  DollarSign,
  Calendar,
  TrendingUp,
  Brain,
  Database,
  FileText,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react'
import './App.css'

// Mock data for demonstration
const mockProjects = [
  {
    id: '1',
    name: 'نظام التعرف على الصور',
    description: 'تطوير نموذج ذكاء اصطناعي للتعرف على الصور باستخدام التعلم العميق',
    status: 'active',
    priority: 'high',
    progress: 75,
    team_size: 5,
    budget: 50000,
    spent_budget: 37500,
    ai_project_category: 'computer_vision',
    technologies: ['Python', 'TensorFlow', 'OpenCV'],
    start_date: '2024-01-15',
    end_date: '2024-06-30'
  },
  {
    id: '2',
    name: 'منصة التجارة الإلكترونية',
    description: 'تطوير منصة تجارة إلكترونية متكاملة مع نظام إدارة المخزون',
    status: 'planning',
    priority: 'medium',
    progress: 25,
    team_size: 8,
    budget: 75000,
    spent_budget: 15000,
    project_type: 'web_development',
    technologies: ['React', 'Node.js', 'MongoDB'],
    start_date: '2024-03-01',
    end_date: '2024-09-30'
  },
  {
    id: '3',
    name: 'تحليل البيانات التنبؤي',
    description: 'نظام تحليل البيانات للتنبؤ بسلوك العملاء واتجاهات السوق',
    status: 'completed',
    priority: 'high',
    progress: 100,
    team_size: 4,
    budget: 40000,
    spent_budget: 38000,
    ai_project_category: 'prediction',
    technologies: ['Python', 'Pandas', 'Scikit-learn'],
    start_date: '2023-10-01',
    end_date: '2024-02-28'
  }
]

const mockTasks = [
  {
    id: '1',
    title: 'تصميم نموذج الشبكة العصبية',
    project_id: '1',
    status: 'in_progress',
    priority: 'high',
    assigned_to: 'أحمد محمد',
    due_date: '2024-07-15',
    progress: 60
  },
  {
    id: '2',
    title: 'جمع وتنظيف البيانات',
    project_id: '1',
    status: 'completed',
    priority: 'medium',
    assigned_to: 'فاطمة علي',
    due_date: '2024-06-30',
    progress: 100
  },
  {
    id: '3',
    title: 'تطوير واجهة المستخدم',
    project_id: '2',
    status: 'todo',
    priority: 'medium',
    assigned_to: 'محمد حسن',
    due_date: '2024-08-15',
    progress: 0
  }
]

const mockUsers = [
  {
    id: '1',
    name: 'أحمد محمد',
    role: 'مطور ذكاء اصطناعي',
    avatar: '',
    status: 'available',
    experience_level: 'senior'
  },
  {
    id: '2',
    name: 'فاطمة علي',
    role: 'محلل بيانات',
    avatar: '',
    status: 'busy',
    experience_level: 'mid'
  },
  {
    id: '3',
    name: 'محمد حسن',
    role: 'مطور واجهات أمامية',
    avatar: '',
    status: 'available',
    experience_level: 'senior'
  }
]

// Components
function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'لوحة التحكم', icon: Home },
    { id: 'projects', label: 'المشاريع', icon: FolderOpen },
    { id: 'tasks', label: 'المهام', icon: CheckCircle },
    { id: 'team', label: 'الفريق', icon: Users },
    { id: 'roles', label: 'الأدوار', icon: UserCheck },
    { id: 'finance', label: 'المالية', icon: DollarSign },
    { id: 'ai-models', label: 'نماذج الذكاء الاصطناعي', icon: Brain },
    { id: 'reports', label: 'التقارير', icon: BarChart3 },
    { id: 'settings', label: 'الإعدادات', icon: Settings }
  ]

  return (
    <div className="w-64 bg-card border-r border-border h-screen p-4">
      <div className="flex items-center gap-2 mb-8">
        <Brain className="h-8 w-8 text-primary" />
        <h1 className="text-xl font-bold">AI Fusion</h1>
      </div>
      
      <nav className="space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <Button
              key={item.id}
              variant={activeTab === item.id ? "default" : "ghost"}
              className="w-full justify-start gap-2"
              onClick={() => setActiveTab(item.id)}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Button>
          )
        })}
      </nav>
    </div>
  )
}

function Header() {
  return (
    <header className="bg-card border-b border-border p-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm">
          <Menu className="h-4 w-4" />
        </Button>
        <div className="relative">
          <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="البحث في المشاريع والمهام..." 
            className="w-80 pr-10"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm">
          <Bell className="h-4 w-4" />
        </Button>
        <Avatar>
          <AvatarFallback>أم</AvatarFallback>
        </Avatar>
      </div>
    </header>
  )
}

function Dashboard() {
  const stats = [
    {
      title: 'إجمالي المشاريع',
      value: '12',
      change: '+2',
      icon: FolderOpen,
      color: 'text-blue-600'
    },
    {
      title: 'المهام المكتملة',
      value: '89',
      change: '+12',
      icon: CheckCircle,
      color: 'text-green-600'
    },
    {
      title: 'أعضاء الفريق',
      value: '24',
      change: '+3',
      icon: Users,
      color: 'text-purple-600'
    },
    {
      title: 'الميزانية المستخدمة',
      value: '75%',
      change: '+5%',
      icon: DollarSign,
      color: 'text-orange-600'
    }
  ]

  return (
    <div className="p-6 space-y-6">
      <div>
        <h2 className="text-3xl font-bold mb-2">مرحباً بك في نظام إدارة المشاريع</h2>
        <p className="text-muted-foreground">نظرة عامة على حالة مشاريعك وفريقك</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <p className="text-xs text-green-600">{stat.change} من الشهر الماضي</p>
                  </div>
                  <Icon className={`h-8 w-8 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>المشاريع النشطة</CardTitle>
            <CardDescription>المشاريع قيد التنفيذ حالياً</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockProjects.filter(p => p.status === 'active').map((project) => (
                <div key={project.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium">{project.name}</h4>
                    <p className="text-sm text-muted-foreground">{project.description}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Badge variant="secondary">{project.ai_project_category}</Badge>
                      <span className="text-xs text-muted-foreground">
                        {project.team_size} أعضاء
                      </span>
                    </div>
                  </div>
                  <div className="text-left">
                    <div className="text-sm font-medium">{project.progress}%</div>
                    <div className="w-20 bg-secondary rounded-full h-2 mt-1">
                      <div 
                        className="bg-primary h-2 rounded-full" 
                        style={{ width: `${project.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>المهام الأخيرة</CardTitle>
            <CardDescription>آخر المهام المحدثة</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockTasks.slice(0, 5).map((task) => (
                <div key={task.id} className="flex items-center gap-3 p-3 border rounded-lg">
                  <div className={`w-3 h-3 rounded-full ${
                    task.status === 'completed' ? 'bg-green-500' :
                    task.status === 'in_progress' ? 'bg-blue-500' : 'bg-gray-300'
                  }`}></div>
                  <div className="flex-1">
                    <h5 className="font-medium text-sm">{task.title}</h5>
                    <p className="text-xs text-muted-foreground">{task.assigned_to}</p>
                  </div>
                  <Badge variant={
                    task.priority === 'high' ? 'destructive' :
                    task.priority === 'medium' ? 'default' : 'secondary'
                  }>
                    {task.priority === 'high' ? 'عالي' :
                     task.priority === 'medium' ? 'متوسط' : 'منخفض'}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function Projects() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">المشاريع</h2>
          <p className="text-muted-foreground">إدارة جميع مشاريعك</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          مشروع جديد
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockProjects.map((project) => (
          <Card key={project.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{project.name}</CardTitle>
                <Badge variant={
                  project.status === 'active' ? 'default' :
                  project.status === 'completed' ? 'secondary' : 'outline'
                }>
                  {project.status === 'active' ? 'نشط' :
                   project.status === 'completed' ? 'مكتمل' : 'تخطيط'}
                </Badge>
              </div>
              <CardDescription>{project.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>التقدم</span>
                    <span>{project.progress}%</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full transition-all" 
                      style={{ width: `${project.progress}%` }}
                    ></div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-1">
                    <Users className="h-4 w-4" />
                    <span>{project.team_size} أعضاء</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <DollarSign className="h-4 w-4" />
                    <span>${project.spent_budget.toLocaleString()}</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1">
                  {project.technologies?.map((tech, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {tech}
                    </Badge>
                  ))}
                </div>

                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <Calendar className="h-3 w-3" />
                  <span>{project.start_date} - {project.end_date}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function Tasks() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">المهام</h2>
          <p className="text-muted-foreground">إدارة وتتبع المهام</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          مهمة جديدة
        </Button>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList>
          <TabsTrigger value="all">جميع المهام</TabsTrigger>
          <TabsTrigger value="todo">قيد الانتظار</TabsTrigger>
          <TabsTrigger value="in_progress">قيد التنفيذ</TabsTrigger>
          <TabsTrigger value="completed">مكتملة</TabsTrigger>
        </TabsList>
        
        <TabsContent value="all" className="space-y-4">
          {mockTasks.map((task) => (
            <Card key={task.id}>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-4 h-4 rounded-full ${
                      task.status === 'completed' ? 'bg-green-500' :
                      task.status === 'in_progress' ? 'bg-blue-500' : 'bg-gray-300'
                    }`}></div>
                    <div>
                      <h4 className="font-medium">{task.title}</h4>
                      <p className="text-sm text-muted-foreground">
                        مُكلف إلى: {task.assigned_to}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <Badge variant={
                      task.priority === 'high' ? 'destructive' :
                      task.priority === 'medium' ? 'default' : 'secondary'
                    }>
                      {task.priority === 'high' ? 'عالي' :
                       task.priority === 'medium' ? 'متوسط' : 'منخفض'}
                    </Badge>
                    
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Clock className="h-4 w-4" />
                      <span>{task.due_date}</span>
                    </div>
                    
                    <div className="text-sm font-medium">
                      {task.progress}%
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  )
}

function Team() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">الفريق</h2>
          <p className="text-muted-foreground">إدارة أعضاء الفريق</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          عضو جديد
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockUsers.map((user) => (
          <Card key={user.id}>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <Avatar className="h-16 w-16">
                  <AvatarImage src={user.avatar} />
                  <AvatarFallback className="text-lg">
                    {user.name.split(' ').map(n => n[0]).join('')}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <h4 className="font-semibold">{user.name}</h4>
                  <p className="text-sm text-muted-foreground">{user.role}</p>
                  <div className="flex items-center gap-2 mt-2">
                    <Badge variant={user.status === 'available' ? 'secondary' : 'outline'}>
                      {user.status === 'available' ? 'متاح' : 'مشغول'}
                    </Badge>
                    <Badge variant="outline">
                      {user.experience_level === 'senior' ? 'خبير' :
                       user.experience_level === 'mid' ? 'متوسط' : 'مبتدئ'}
                    </Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />
      case 'projects':
        return <ProjectManagement />
      case 'tasks':
        return <Tasks />
      case 'team':
        return <Team />
      case 'roles':
        return <RoleManagement />
      case 'finance':
        return <FinanceManagement />
      case 'ai-models':
        return <div className="p-6"><h2 className="text-3xl font-bold">نماذج الذكاء الاصطناعي</h2><p>قريباً...</p></div>
      case 'reports':
        return <div className="p-6"><h2 className="text-3xl font-bold">التقارير</h2><p>قريباً...</p></div>
      case 'settings':
        return <div className="p-6"><h2 className="text-3xl font-bold">الإعدادات</h2><p>قريباً...</p></div>
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-background text-foreground" dir="rtl">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  )
}

export default App

