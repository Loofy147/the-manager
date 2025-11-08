import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Plus, 
  Edit, 
  Trash2, 
  Users, 
  Calendar, 
  DollarSign,
  Brain,
  Database,
  Code,
  BarChart3,
  Clock,
  CheckCircle,
  AlertCircle,
  Star,
  Filter,
  Search,
  Download,
  Upload,
  Settings,
  Eye,
  Play,
  Pause,
  Square,
  GitBranch,
  Cpu,
  Zap,
  Target,
  TrendingUp,
  FileText,
  Link,
  Globe,
  MessageSquare
} from 'lucide-react'

// Enhanced mock data for AI projects
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
    project_type: 'ai_project',
    ai_category: 'computer_vision',
    technologies: ['Python', 'TensorFlow', 'OpenCV', 'CUDA'],
    start_date: '2024-01-15',
    end_date: '2024-06-30',
    client: 'شركة التقنيات المتقدمة',
    project_manager: 'أحمد محمد',
    datasets: [
      { name: 'ImageNet', size: '150GB', status: 'processed' },
      { name: 'COCO Dataset', size: '25GB', status: 'processing' }
    ],
    models: [
      { name: 'ResNet-50', accuracy: '94.2%', status: 'trained' },
      { name: 'EfficientNet-B7', accuracy: '96.1%', status: 'training' }
    ],
    milestones: [
      { name: 'جمع البيانات', status: 'completed', date: '2024-02-15' },
      { name: 'تدريب النموذج', status: 'in_progress', date: '2024-04-30' },
      { name: 'اختبار الأداء', status: 'pending', date: '2024-05-30' }
    ],
    risks: [
      { description: 'نقص في البيانات التدريبية', severity: 'medium', mitigation: 'البحث عن مصادر إضافية' },
      { description: 'تأخير في الحصول على GPU', severity: 'high', mitigation: 'استخدام خدمات السحابة' }
    ]
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
    technologies: ['React', 'Node.js', 'MongoDB', 'Redis'],
    start_date: '2024-03-01',
    end_date: '2024-09-30',
    client: 'متجر الإلكترونيات الذكية',
    project_manager: 'فاطمة علي',
    milestones: [
      { name: 'تصميم الواجهات', status: 'completed', date: '2024-03-15' },
      { name: 'تطوير الخلفية', status: 'in_progress', date: '2024-06-01' },
      { name: 'اختبار النظام', status: 'pending', date: '2024-08-15' }
    ]
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
    project_type: 'ai_project',
    ai_category: 'prediction',
    technologies: ['Python', 'Pandas', 'Scikit-learn', 'Apache Spark'],
    start_date: '2023-10-01',
    end_date: '2024-02-28',
    client: 'بنك الاستثمار الوطني',
    project_manager: 'محمد حسن',
    models: [
      { name: 'LSTM Predictor', accuracy: '89.5%', status: 'deployed' },
      { name: 'Random Forest', accuracy: '87.2%', status: 'backup' }
    ]
  }
]

const mockTasks = [
  {
    id: '1',
    title: 'تصميم نموذج الشبكة العصبية',
    description: 'تصميم وتطوير بنية الشبكة العصبية للتعرف على الصور',
    project_id: '1',
    status: 'in_progress',
    priority: 'high',
    assigned_to: 'أحمد محمد',
    assigned_to_id: '1',
    due_date: '2024-07-15',
    progress: 60,
    estimated_hours: 40,
    actual_hours: 24,
    tags: ['deep_learning', 'neural_networks', 'architecture'],
    dependencies: [],
    subtasks: [
      { id: '1a', title: 'اختيار بنية الشبكة', status: 'completed' },
      { id: '1b', title: 'تحديد المعاملات', status: 'in_progress' },
      { id: '1c', title: 'اختبار الأداء الأولي', status: 'pending' }
    ]
  },
  {
    id: '2',
    title: 'جمع وتنظيف البيانات',
    description: 'جمع البيانات من مصادر متعددة وتنظيفها للتدريب',
    project_id: '1',
    status: 'completed',
    priority: 'medium',
    assigned_to: 'فاطمة علي',
    assigned_to_id: '2',
    due_date: '2024-06-30',
    progress: 100,
    estimated_hours: 30,
    actual_hours: 28,
    tags: ['data_processing', 'cleaning', 'preprocessing']
  },
  {
    id: '3',
    title: 'تطوير واجهة المستخدم',
    description: 'تصميم وتطوير واجهة المستخدم للمنصة',
    project_id: '2',
    status: 'todo',
    priority: 'medium',
    assigned_to: 'محمد حسن',
    assigned_to_id: '3',
    due_date: '2024-08-15',
    progress: 0,
    estimated_hours: 60,
    actual_hours: 0,
    tags: ['frontend', 'ui_design', 'react'],
    comments: [
        {
            id: '1',
            user: 'Ahmed',
            avatar: 'https://i.pravatar.cc/40',
            timestamp: '2 hours ago',
            content: 'I think we should use a different approach here.'
        }
    ]
  }
]
function TaskItem({ task }) {
  const [showComments, setShowComments] = useState(false)

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
            <h4 className="font-medium">{task.title}</h4>
            <div className="flex items-center gap-2">
                <Badge>{task.status}</Badge>
                <Button variant="ghost" size="sm" onClick={() => setShowComments(!showComments)}>
                    <MessageSquare className="h-4 w-4" />
                </Button>
            </div>
        </div>
        <p className="text-sm text-muted-foreground mt-2">{task.description}</p>
        {showComments && (
            <div className="mt-4 space-y-4">
                <h5 className="font-medium">Comments</h5>
                {task.comments.map(comment => (
                    <div key={comment.id} className="flex items-start gap-3">
                        <img src={comment.avatar} alt={comment.user} className="w-8 h-8 rounded-full" />
                        <div className="flex-1">
                            <div className="flex items-center justify-between">
                                <span className="font-medium text-sm">{comment.user}</span>
                                <span className="text-xs text-muted-foreground">{comment.timestamp}</span>
                            </div>
                            <p className="text-sm">{comment.content}</p>
                        </div>
                    </div>
                ))}
                <div className="flex gap-2">
                    <Input placeholder="Add a comment..." />
                    <Button>Send</Button>
                </div>
            </div>
        )}
      </CardContent>
    </Card>
  )
}
const aiCategories = [
  { id: 'computer_vision', name: 'رؤية الحاسوب', icon: Eye },
  { id: 'nlp', name: 'معالجة اللغة الطبيعية', icon: FileText },
  { id: 'prediction', name: 'التنبؤ والتحليل', icon: TrendingUp },
  { id: 'recommendation', name: 'أنظمة التوصية', icon: Target },
  { id: 'robotics', name: 'الروبوتات', icon: Cpu },
  { id: 'speech', name: 'معالجة الصوت', icon: Zap }
]

const projectStatuses = [
  { id: 'planning', name: 'تخطيط', color: 'bg-yellow-500' },
  { id: 'active', name: 'نشط', color: 'bg-green-500' },
  { id: 'on_hold', name: 'متوقف', color: 'bg-orange-500' },
  { id: 'completed', name: 'مكتمل', color: 'bg-blue-500' },
  { id: 'cancelled', name: 'ملغي', color: 'bg-red-500' }
]

function ProjectCard({ project, onEdit, onDelete, onViewDetails }) {
  const statusConfig = projectStatuses.find(s => s.id === project.status)
  const aiCategory = aiCategories.find(c => c.id === project.ai_category)
  
  return (
    <Card className="hover:shadow-lg transition-all duration-200 border-l-4" 
          style={{ borderLeftColor: statusConfig?.color.replace('bg-', '#') }}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <CardTitle className="text-lg">{project.name}</CardTitle>
              {project.project_type === 'ai_project' && (
                <Brain className="h-5 w-5 text-purple-600" />
              )}
            </div>
            <CardDescription className="text-sm">{project.description}</CardDescription>
          </div>
          <div className="flex flex-col gap-2">
            <Badge variant={
              project.priority === 'high' ? 'destructive' :
              project.priority === 'medium' ? 'default' : 'secondary'
            }>
              {project.priority === 'high' ? 'عالي' :
               project.priority === 'medium' ? 'متوسط' : 'منخفض'}
            </Badge>
            <Badge variant="outline" className={statusConfig?.color}>
              {statusConfig?.name}
            </Badge>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Progress */}
        <div>
          <div className="flex justify-between text-sm mb-2">
            <span>التقدم</span>
            <span>{project.progress}%</span>
          </div>
          <Progress value={project.progress} className="h-2" />
        </div>

        {/* AI Category */}
        {project.ai_category && aiCategory && (
          <div className="flex items-center gap-2 text-sm">
            <aiCategory.icon className="h-4 w-4 text-purple-600" />
            <span>{aiCategory.name}</span>
          </div>
        )}

        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4 text-blue-500" />
            <span>{project.team_size} أعضاء</span>
          </div>
          <div className="flex items-center gap-2">
            <DollarSign className="h-4 w-4 text-green-500" />
            <span>${project.spent_budget.toLocaleString()}</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-orange-500" />
            <span>{new Date(project.end_date).toLocaleDateString('ar')}</span>
          </div>
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4 text-gray-500" />
            <span>{project.project_manager}</span>
          </div>
        </div>

        {/* Technologies */}
        <div className="flex flex-wrap gap-1">
          {project.technologies?.slice(0, 4).map((tech, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {tech}
            </Badge>
          ))}
          {project.technologies?.length > 4 && (
            <Badge variant="outline" className="text-xs">
              +{project.technologies.length - 4}
            </Badge>
          )}
        </div>

        {/* AI Models (for AI projects) */}
        {project.models && project.models.length > 0 && (
          <div className="space-y-2">
            <h5 className="text-sm font-medium">النماذج:</h5>
            {project.models.slice(0, 2).map((model, index) => (
              <div key={index} className="flex items-center justify-between text-xs bg-gray-50 p-2 rounded">
                <span>{model.name}</span>
                <div className="flex items-center gap-2">
                  {model.accuracy && <span className="text-green-600">{model.accuracy}</span>}
                  <Badge variant="outline" size="sm">
                    {model.status === 'trained' ? 'مدرب' :
                     model.status === 'training' ? 'قيد التدريب' :
                     model.status === 'deployed' ? 'منشور' : model.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          <Button variant="outline" size="sm" onClick={() => onViewDetails(project)}>
            <Eye className="h-4 w-4 ml-1" />
            عرض
          </Button>
          <Button variant="outline" size="sm" onClick={() => onEdit(project)}>
            <Edit className="h-4 w-4 ml-1" />
            تعديل
          </Button>
          {project.status !== 'active' && (
            <Button variant="outline" size="sm" onClick={() => onDelete(project)}>
              <Trash2 className="h-4 w-4 ml-1" />
              حذف
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

function CreateProjectDialog({ open, onOpenChange }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    project_type: 'web_development',
    ai_category: '',
    priority: 'medium',
    budget: 0,
    start_date: '',
    end_date: '',
    client: '',
    project_manager: '',
    technologies: [],
    team_members: []
  })

  const [newTechnology, setNewTechnology] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Creating project:', formData)
    onOpenChange(false)
    // Here you would call the API to create the project
  }

  const addTechnology = () => {
    if (newTechnology && !formData.technologies.includes(newTechnology)) {
      setFormData(prev => ({
        ...prev,
        technologies: [...prev.technologies, newTechnology]
      }))
      setNewTechnology('')
    }
  }

  const removeTechnology = (tech) => {
    setFormData(prev => ({
      ...prev,
      technologies: prev.technologies.filter(t => t !== tech)
    }))
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>إنشاء مشروع جديد</DialogTitle>
          <DialogDescription>
            إنشاء مشروع جديد في النظام مع تحديد جميع التفاصيل المطلوبة
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <Tabs defaultValue="basic" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="basic">المعلومات الأساسية</TabsTrigger>
              <TabsTrigger value="technical">التفاصيل التقنية</TabsTrigger>
              <TabsTrigger value="team">الفريق والموارد</TabsTrigger>
              <TabsTrigger value="timeline">الجدولة والميزانية</TabsTrigger>
            </TabsList>
            
            <TabsContent value="basic" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">اسم المشروع</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="مثال: نظام إدارة المخزون الذكي"
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="client">العميل</Label>
                  <Input
                    id="client"
                    value={formData.client}
                    onChange={(e) => setFormData(prev => ({ ...prev, client: e.target.value }))}
                    placeholder="اسم العميل أو الشركة"
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="description">وصف المشروع</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="وصف مفصل لأهداف ومتطلبات المشروع"
                  rows={4}
                  required
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="project_type">نوع المشروع</Label>
                  <Select value={formData.project_type} onValueChange={(value) => setFormData(prev => ({ ...prev, project_type: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="اختر نوع المشروع" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ai_project">مشروع ذكاء اصطناعي</SelectItem>
                      <SelectItem value="web_development">تطوير ويب</SelectItem>
                      <SelectItem value="mobile_development">تطوير تطبيقات الجوال</SelectItem>
                      <SelectItem value="data_analysis">تحليل البيانات</SelectItem>
                      <SelectItem value="consulting">استشارات</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                {formData.project_type === 'ai_project' && (
                  <div className="space-y-2">
                    <Label htmlFor="ai_category">فئة الذكاء الاصطناعي</Label>
                    <Select value={formData.ai_category} onValueChange={(value) => setFormData(prev => ({ ...prev, ai_category: value }))}>
                      <SelectTrigger>
                        <SelectValue placeholder="اختر فئة الذكاء الاصطناعي" />
                      </SelectTrigger>
                      <SelectContent>
                        {aiCategories.map((category) => (
                          <SelectItem key={category.id} value={category.id}>
                            {category.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
                
                <div className="space-y-2">
                  <Label htmlFor="priority">الأولوية</Label>
                  <Select value={formData.priority} onValueChange={(value) => setFormData(prev => ({ ...prev, priority: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="اختر الأولوية" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">منخفضة</SelectItem>
                      <SelectItem value="medium">متوسطة</SelectItem>
                      <SelectItem value="high">عالية</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="technical" className="space-y-4">
              <div className="space-y-4">
                <Label>التقنيات المستخدمة</Label>
                <div className="flex gap-2">
                  <Input
                    value={newTechnology}
                    onChange={(e) => setNewTechnology(e.target.value)}
                    placeholder="أضف تقنية جديدة"
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTechnology())}
                  />
                  <Button type="button" onClick={addTechnology}>
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.technologies.map((tech, index) => (
                    <Badge key={index} variant="secondary" className="cursor-pointer" onClick={() => removeTechnology(tech)}>
                      {tech} ×
                    </Badge>
                  ))}
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="team" className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="project_manager">مدير المشروع</Label>
                <Select value={formData.project_manager} onValueChange={(value) => setFormData(prev => ({ ...prev, project_manager: value }))}>
                  <SelectTrigger>
                    <SelectValue placeholder="اختر مدير المشروع" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="أحمد محمد">أحمد محمد</SelectItem>
                    <SelectItem value="فاطمة علي">فاطمة علي</SelectItem>
                    <SelectItem value="محمد حسن">محمد حسن</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </TabsContent>
            
            <TabsContent value="timeline" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="start_date">تاريخ البداية</Label>
                  <Input
                    id="start_date"
                    type="date"
                    value={formData.start_date}
                    onChange={(e) => setFormData(prev => ({ ...prev, start_date: e.target.value }))}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="end_date">تاريخ النهاية المتوقع</Label>
                  <Input
                    id="end_date"
                    type="date"
                    value={formData.end_date}
                    onChange={(e) => setFormData(prev => ({ ...prev, end_date: e.target.value }))}
                    required
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="budget">الميزانية ($)</Label>
                <Input
                  id="budget"
                  type="number"
                  value={formData.budget}
                  onChange={(e) => setFormData(prev => ({ ...prev, budget: parseInt(e.target.value) }))}
                  placeholder="0"
                  min="0"
                />
              </div>
            </TabsContent>
          </Tabs>
          
          <div className="flex gap-2">
            <Button type="submit">إنشاء المشروع</Button>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              إلغاء
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

function ProjectDetailsDialog({ open, onOpenChange, project }) {
  if (!project) return null

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {project.project_type === 'ai_project' && <Brain className="h-6 w-6 text-purple-600" />}
            {project.name}
          </DialogTitle>
          <DialogDescription>{project.description}</DialogDescription>
        </DialogHeader>
        
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
            <TabsTrigger value="tasks">المهام</TabsTrigger>
            <TabsTrigger value="team">الفريق</TabsTrigger>
            <TabsTrigger value="ai-models">النماذج</TabsTrigger>
            <TabsTrigger value="risks">المخاطر</TabsTrigger>
          </TabsList>
          
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
          </TabsContent>

          <TabsContent value="tasks" className="space-y-4">
            {mockTasks.filter(task => task.project_id === project.id).map(task => (
              <TaskItem key={task.id} task={task} />
            ))}
                  <CardTitle className="text-lg">التقدم العام</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-primary">{project.progress}%</div>
                      <Progress value={project.progress} className="mt-2" />
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">الحالة:</span>
                        <div className="font-medium">
                          {projectStatuses.find(s => s.id === project.status)?.name}
                        </div>
                      </div>
                      <div>
                        <span className="text-muted-foreground">الأولوية:</span>
                        <div className="font-medium">
                          {project.priority === 'high' ? 'عالية' :
                           project.priority === 'medium' ? 'متوسطة' : 'منخفضة'}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">الميزانية</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold">${project.spent_budget.toLocaleString()}</div>
                      <div className="text-sm text-muted-foreground">من ${project.budget.toLocaleString()}</div>
                      <Progress value={(project.spent_budget / project.budget) * 100} className="mt-2" />
                    </div>
                    <div className="text-sm">
                      <span className="text-muted-foreground">المتبقي: </span>
                      <span className="font-medium">${(project.budget - project.spent_budget).toLocaleString()}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">الجدولة</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-muted-foreground">البداية:</span>
                      <div className="font-medium">{new Date(project.start_date).toLocaleDateString('ar')}</div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">النهاية:</span>
                      <div className="font-medium">{new Date(project.end_date).toLocaleDateString('ar')}</div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">المدة:</span>
                      <div className="font-medium">
                        {Math.ceil((new Date(project.end_date) - new Date(project.start_date)) / (1000 * 60 * 60 * 24))} يوم
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
            
            {/* Milestones */}
            {project.milestones && (
              <Card>
                <CardHeader>
                  <CardTitle>المعالم الرئيسية</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {project.milestones.map((milestone, index) => (
                      <div key={index} className="flex items-center gap-4 p-3 border rounded-lg">
                        <div className={`w-4 h-4 rounded-full ${
                          milestone.status === 'completed' ? 'bg-green-500' :
                          milestone.status === 'in_progress' ? 'bg-blue-500' : 'bg-gray-300'
                        }`}></div>
                        <div className="flex-1">
                          <h4 className="font-medium">{milestone.name}</h4>
                          <p className="text-sm text-muted-foreground">{milestone.date}</p>
                        </div>
                        <Badge variant={
                          milestone.status === 'completed' ? 'secondary' :
                          milestone.status === 'in_progress' ? 'default' : 'outline'
                        }>
                          {milestone.status === 'completed' ? 'مكتمل' :
                           milestone.status === 'in_progress' ? 'قيد التنفيذ' : 'معلق'}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
          
          <TabsContent value="ai-models" className="space-y-6">
            {project.models && project.models.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {project.models.map((model, index) => (
                  <Card key={index}>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <span>{model.name}</span>
                        <Badge variant={
                          model.status === 'deployed' ? 'secondary' :
                          model.status === 'trained' ? 'default' : 'outline'
                        }>
                          {model.status === 'trained' ? 'مدرب' :
                           model.status === 'training' ? 'قيد التدريب' :
                           model.status === 'deployed' ? 'منشور' : model.status}
                        </Badge>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {model.accuracy && (
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span>الدقة</span>
                              <span className="font-medium text-green-600">{model.accuracy}</span>
                            </div>
                            <Progress value={parseFloat(model.accuracy)} className="h-2" />
                          </div>
                        )}
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4 ml-1" />
                            عرض التفاصيل
                          </Button>
                          {model.status === 'trained' && (
                            <Button variant="outline" size="sm">
                              <Play className="h-4 w-4 ml-1" />
                              نشر
                            </Button>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Brain className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">لا توجد نماذج ذكاء اصطناعي في هذا المشروع</p>
              </div>
            )}
          </TabsContent>
          
          <TabsContent value="risks" className="space-y-6">
            {project.risks && project.risks.length > 0 ? (
              <div className="space-y-4">
                {project.risks.map((risk, index) => (
                  <Card key={index}>
                    <CardContent className="p-4">
                      <div className="flex items-start gap-4">
                        <AlertCircle className={`h-5 w-5 mt-1 ${
                          risk.severity === 'high' ? 'text-red-500' :
                          risk.severity === 'medium' ? 'text-yellow-500' : 'text-blue-500'
                        }`} />
                        <div className="flex-1">
                          <h4 className="font-medium">{risk.description}</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            <strong>الحل:</strong> {risk.mitigation}
                          </p>
                        </div>
                        <Badge variant={
                          risk.severity === 'high' ? 'destructive' :
                          risk.severity === 'medium' ? 'default' : 'secondary'
                        }>
                          {risk.severity === 'high' ? 'عالي' :
                           risk.severity === 'medium' ? 'متوسط' : 'منخفض'}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
                <p className="text-muted-foreground">لا توجد مخاطر محددة لهذا المشروع</p>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}

export default function ProjectManagement() {
  const [projects, setProjects] = useState(mockProjects)
  const [filteredProjects, setFilteredProjects] = useState(mockProjects)
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false)
  const [selectedProject, setSelectedProject] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')

  useEffect(() => {
    let filtered = projects

    if (searchTerm) {
      filtered = filtered.filter(project =>
        project.name.includes(searchTerm) ||
        project.description.includes(searchTerm) ||
        project.client?.includes(searchTerm)
      )
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(project => project.status === statusFilter)
    }

    if (typeFilter !== 'all') {
      filtered = filtered.filter(project => project.project_type === typeFilter)
    }

    setFilteredProjects(filtered)
  }, [projects, searchTerm, statusFilter, typeFilter])

  const handleEditProject = (project) => {
    console.log('Editing project:', project)
    // Here you would open an edit dialog
  }

  const handleDeleteProject = (project) => {
    console.log('Deleting project:', project)
    // Here you would call the API to delete the project
  }

  const handleViewDetails = (project) => {
    setSelectedProject(project)
    setDetailsDialogOpen(true)
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">إدارة المشاريع</h2>
          <p className="text-muted-foreground">إدارة وتتبع جميع المشاريع والمبادرات</p>
        </div>
        <Button onClick={() => setCreateDialogOpen(true)}>
          <Plus className="h-4 w-4 ml-2" />
          مشروع جديد
        </Button>
      </div>

      {/* Filters and Search */}
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="البحث في المشاريع..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pr-10"
            />
          </div>
        </div>
        
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="الحالة" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">جميع الحالات</SelectItem>
            {projectStatuses.map((status) => (
              <SelectItem key={status.id} value={status.id}>
                {status.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        
        <Select value={typeFilter} onValueChange={setTypeFilter}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="النوع" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">جميع الأنواع</SelectItem>
            <SelectItem value="ai_project">ذكاء اصطناعي</SelectItem>
            <SelectItem value="web_development">تطوير ويب</SelectItem>
            <SelectItem value="mobile_development">تطبيقات الجوال</SelectItem>
            <SelectItem value="data_analysis">تحليل البيانات</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            onEdit={handleEditProject}
            onDelete={handleDeleteProject}
            onViewDetails={handleViewDetails}
          />
        ))}
      </div>

      {filteredProjects.length === 0 && (
        <div className="text-center py-12">
          <FolderOpen className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <p className="text-muted-foreground">لا توجد مشاريع تطابق المعايير المحددة</p>
        </div>
      )}

      <CreateProjectDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
      />

      <ProjectDetailsDialog
        open={detailsDialogOpen}
        onOpenChange={setDetailsDialogOpen}
        project={selectedProject}
      />
    </div>
  )
}

