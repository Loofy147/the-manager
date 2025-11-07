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
import { 
  Plus, 
  Edit, 
  Trash2, 
  Users, 
  Shield, 
  ChevronDown, 
  ChevronRight,
  UserPlus,
  Settings,
  Eye,
  Lock,
  Unlock
} from 'lucide-react'

// Mock data for roles hierarchy
const mockRoles = [
  {
    id: '1',
    name: 'المدير العام',
    description: 'المسؤول الأعلى في النظام',
    level: 0,
    path: '/المدير العام',
    parent_role_id: null,
    permissions: ['all'],
    can_create_subroles: true,
    can_assign_roles: true,
    can_manage_projects: true,
    can_manage_budgets: true,
    can_view_reports: true,
    max_subordinates: 10,
    assigned_users: 1,
    subroles: [
      {
        id: '2',
        name: 'مدير المشاريع',
        description: 'مسؤول عن إدارة المشاريع',
        level: 1,
        path: '/المدير العام/مدير المشاريع',
        parent_role_id: '1',
        permissions: ['project_management', 'team_management'],
        can_create_subroles: true,
        can_assign_roles: false,
        can_manage_projects: true,
        can_manage_budgets: false,
        can_view_reports: true,
        max_subordinates: 5,
        assigned_users: 2,
        subroles: [
          {
            id: '3',
            name: 'قائد فريق',
            description: 'قائد فريق تطوير',
            level: 2,
            path: '/المدير العام/مدير المشاريع/قائد فريق',
            parent_role_id: '2',
            permissions: ['task_management', 'team_coordination'],
            can_create_subroles: false,
            can_assign_roles: false,
            can_manage_projects: false,
            can_manage_budgets: false,
            can_view_reports: false,
            max_subordinates: 8,
            assigned_users: 3,
            subroles: []
          }
        ]
      },
      {
        id: '4',
        name: 'مدير الموارد البشرية',
        description: 'مسؤول عن إدارة الموارد البشرية',
        level: 1,
        path: '/المدير العام/مدير الموارد البشرية',
        parent_role_id: '1',
        permissions: ['hr_management', 'user_management'],
        can_create_subroles: true,
        can_assign_roles: true,
        can_manage_projects: false,
        can_manage_budgets: false,
        can_view_reports: true,
        max_subordinates: 3,
        assigned_users: 1,
        subroles: []
      }
    ]
  }
]

const permissions = [
  { id: 'project_management', name: 'إدارة المشاريع', description: 'إنشاء وتعديل وحذف المشاريع' },
  { id: 'task_management', name: 'إدارة المهام', description: 'إنشاء وتعديل وحذف المهام' },
  { id: 'user_management', name: 'إدارة المستخدمين', description: 'إضافة وتعديل المستخدمين' },
  { id: 'role_management', name: 'إدارة الأدوار', description: 'إنشاء وتعديل الأدوار' },
  { id: 'budget_management', name: 'إدارة الميزانية', description: 'إدارة الميزانيات والتكاليف' },
  { id: 'report_viewing', name: 'عرض التقارير', description: 'الوصول إلى التقارير والإحصائيات' },
  { id: 'team_coordination', name: 'تنسيق الفريق', description: 'تنسيق العمل بين أعضاء الفريق' },
  { id: 'hr_management', name: 'إدارة الموارد البشرية', description: 'إدارة شؤون الموظفين' }
]

function RoleCard({ role, onEdit, onDelete, onAssignUsers, level = 0 }) {
  const [expanded, setExpanded] = useState(true)
  
  return (
    <div className={`ml-${level * 6}`}>
      <Card className="mb-4">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {role.subroles && role.subroles.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setExpanded(!expanded)}
                >
                  {expanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                </Button>
              )}
              <div>
                <CardTitle className="text-lg">{role.name}</CardTitle>
                <CardDescription>{role.description}</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline">المستوى {role.level}</Badge>
              <Badge variant="secondary">{role.assigned_users} مستخدم</Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-blue-500" />
                <span>الصلاحيات: {role.permissions.length}</span>
              </div>
              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-green-500" />
                <span>الحد الأقصى: {role.max_subordinates}</span>
              </div>
              <div className="flex items-center gap-2">
                {role.can_create_subroles ? <Unlock className="h-4 w-4 text-green-500" /> : <Lock className="h-4 w-4 text-red-500" />}
                <span>إنشاء أدوار فرعية</span>
              </div>
              <div className="flex items-center gap-2">
                {role.can_assign_roles ? <Unlock className="h-4 w-4 text-green-500" /> : <Lock className="h-4 w-4 text-red-500" />}
                <span>تعيين الأدوار</span>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-1">
              {role.permissions.slice(0, 5).map((permission, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {permissions.find(p => p.id === permission)?.name || permission}
                </Badge>
              ))}
              {role.permissions.length > 5 && (
                <Badge variant="outline" className="text-xs">
                  +{role.permissions.length - 5} المزيد
                </Badge>
              )}
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={() => onEdit(role)}>
                <Edit className="h-4 w-4 ml-1" />
                تعديل
              </Button>
              <Button variant="outline" size="sm" onClick={() => onAssignUsers(role)}>
                <UserPlus className="h-4 w-4 ml-1" />
                تعيين مستخدمين
              </Button>
              {role.assigned_users === 0 && (
                <Button variant="outline" size="sm" onClick={() => onDelete(role)}>
                  <Trash2 className="h-4 w-4 ml-1" />
                  حذف
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
      
      {expanded && role.subroles && role.subroles.map((subrole) => (
        <RoleCard
          key={subrole.id}
          role={subrole}
          onEdit={onEdit}
          onDelete={onDelete}
          onAssignUsers={onAssignUsers}
          level={level + 1}
        />
      ))}
    </div>
  )
}

function CreateRoleDialog({ open, onOpenChange, parentRole = null }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    parent_role_id: parentRole?.id || '',
    permissions: [],
    max_subordinates: 0,
    can_create_subroles: false,
    can_assign_roles: false,
    can_manage_projects: false,
    can_manage_budgets: false,
    can_view_reports: false
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Creating role:', formData)
    onOpenChange(false)
    // Here you would call the API to create the role
  }

  const handlePermissionChange = (permissionId, checked) => {
    setFormData(prev => ({
      ...prev,
      permissions: checked 
        ? [...prev.permissions, permissionId]
        : prev.permissions.filter(p => p !== permissionId)
    }))
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>إنشاء دور جديد</DialogTitle>
          <DialogDescription>
            {parentRole ? `إنشاء دور فرعي تحت: ${parentRole.name}` : 'إنشاء دور جديد في النظام'}
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">اسم الدور</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="مثال: مطور واجهات أمامية"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="max_subordinates">الحد الأقصى للمرؤوسين</Label>
              <Input
                id="max_subordinates"
                type="number"
                value={formData.max_subordinates}
                onChange={(e) => setFormData(prev => ({ ...prev, max_subordinates: parseInt(e.target.value) }))}
                min="0"
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="description">الوصف</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="وصف مختصر لمسؤوليات هذا الدور"
              rows={3}
            />
          </div>
          
          <div className="space-y-4">
            <Label>الصلاحيات الأساسية</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="can_create_subroles"
                  checked={formData.can_create_subroles}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, can_create_subroles: checked }))}
                />
                <Label htmlFor="can_create_subroles" className="text-sm">
                  يمكن إنشاء أدوار فرعية
                </Label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="can_assign_roles"
                  checked={formData.can_assign_roles}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, can_assign_roles: checked }))}
                />
                <Label htmlFor="can_assign_roles" className="text-sm">
                  يمكن تعيين الأدوار
                </Label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="can_manage_projects"
                  checked={formData.can_manage_projects}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, can_manage_projects: checked }))}
                />
                <Label htmlFor="can_manage_projects" className="text-sm">
                  يمكن إدارة المشاريع
                </Label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="can_manage_budgets"
                  checked={formData.can_manage_budgets}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, can_manage_budgets: checked }))}
                />
                <Label htmlFor="can_manage_budgets" className="text-sm">
                  يمكن إدارة الميزانيات
                </Label>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="can_view_reports"
                  checked={formData.can_view_reports}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, can_view_reports: checked }))}
                />
                <Label htmlFor="can_view_reports" className="text-sm">
                  يمكن عرض التقارير
                </Label>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <Label>الصلاحيات التفصيلية</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-40 overflow-y-auto">
              {permissions.map((permission) => (
                <div key={permission.id} className="flex items-start space-x-2">
                  <Checkbox
                    id={permission.id}
                    checked={formData.permissions.includes(permission.id)}
                    onCheckedChange={(checked) => handlePermissionChange(permission.id, checked)}
                  />
                  <div className="space-y-1">
                    <Label htmlFor={permission.id} className="text-sm font-medium">
                      {permission.name}
                    </Label>
                    <p className="text-xs text-muted-foreground">
                      {permission.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="flex gap-2">
            <Button type="submit">إنشاء الدور</Button>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              إلغاء
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

function AssignUsersDialog({ open, onOpenChange, role }) {
  const [selectedUsers, setSelectedUsers] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  
  // Mock users data
  const availableUsers = [
    { id: '1', name: 'أحمد محمد', email: 'ahmed@example.com', current_role: 'مطور' },
    { id: '2', name: 'فاطمة علي', email: 'fatima@example.com', current_role: 'محلل بيانات' },
    { id: '3', name: 'محمد حسن', email: 'mohamed@example.com', current_role: 'مصمم' },
    { id: '4', name: 'سارة أحمد', email: 'sara@example.com', current_role: 'مطور واجهات' }
  ]

  const filteredUsers = availableUsers.filter(user =>
    user.name.includes(searchTerm) || user.email.includes(searchTerm)
  )

  const handleAssign = () => {
    console.log('Assigning users to role:', { role: role?.id, users: selectedUsers })
    onOpenChange(false)
    // Here you would call the API to assign users to the role
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>تعيين مستخدمين للدور</DialogTitle>
          <DialogDescription>
            تعيين مستخدمين للدور: {role?.name}
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="search">البحث عن المستخدمين</Label>
            <Input
              id="search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="البحث بالاسم أو البريد الإلكتروني"
            />
          </div>
          
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {filteredUsers.map((user) => (
              <div key={user.id} className="flex items-center space-x-2 p-2 border rounded">
                <Checkbox
                  id={user.id}
                  checked={selectedUsers.includes(user.id)}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      setSelectedUsers(prev => [...prev, user.id])
                    } else {
                      setSelectedUsers(prev => prev.filter(id => id !== user.id))
                    }
                  }}
                />
                <div className="flex-1">
                  <Label htmlFor={user.id} className="font-medium">
                    {user.name}
                  </Label>
                  <p className="text-xs text-muted-foreground">{user.email}</p>
                  <p className="text-xs text-muted-foreground">الدور الحالي: {user.current_role}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="flex gap-2">
            <Button onClick={handleAssign} disabled={selectedUsers.length === 0}>
              تعيين ({selectedUsers.length})
            </Button>
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              إلغاء
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default function RoleManagement() {
  const [roles, setRoles] = useState(mockRoles)
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [assignDialogOpen, setAssignDialogOpen] = useState(false)
  const [selectedRole, setSelectedRole] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  const handleEditRole = (role) => {
    console.log('Editing role:', role)
    // Here you would open an edit dialog or navigate to edit page
  }

  const handleDeleteRole = (role) => {
    console.log('Deleting role:', role)
    // Here you would call the API to delete the role
  }

  const handleAssignUsers = (role) => {
    setSelectedRole(role)
    setAssignDialogOpen(true)
  }

  const flattenRoles = (roles) => {
    let flattened = []
    roles.forEach(role => {
      flattened.push(role)
      if (role.subroles) {
        flattened = flattened.concat(flattenRoles(role.subroles))
      }
    })
    return flattened
  }

  const filteredRoles = searchTerm 
    ? flattenRoles(roles).filter(role => 
        role.name.includes(searchTerm) || 
        role.description.includes(searchTerm)
      )
    : roles

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">إدارة الأدوار</h2>
          <p className="text-muted-foreground">إدارة الأدوار والصلاحيات في النظام</p>
        </div>
        <Button onClick={() => setCreateDialogOpen(true)}>
          <Plus className="h-4 w-4 ml-2" />
          دور جديد
        </Button>
      </div>

      <div className="flex gap-4">
        <div className="flex-1">
          <Input
            placeholder="البحث في الأدوار..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {searchTerm ? (
          // Show flat list when searching
          filteredRoles.map((role) => (
            <RoleCard
              key={role.id}
              role={role}
              onEdit={handleEditRole}
              onDelete={handleDeleteRole}
              onAssignUsers={handleAssignUsers}
              level={0}
            />
          ))
        ) : (
          // Show hierarchical structure when not searching
          roles.map((role) => (
            <RoleCard
              key={role.id}
              role={role}
              onEdit={handleEditRole}
              onDelete={handleDeleteRole}
              onAssignUsers={handleAssignUsers}
              level={0}
            />
          ))
        )}
      </div>

      <CreateRoleDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
      />

      <AssignUsersDialog
        open={assignDialogOpen}
        onOpenChange={setAssignDialogOpen}
        role={selectedRole}
      />
    </div>
  )
}

