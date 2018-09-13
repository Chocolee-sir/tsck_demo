from django.db import models

# Create your models here.


######################用户管理########################
class User(models.Model):
    """用户表"""
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    realname = models.CharField(max_length=64)
    sex_choices = (
        (0, '女'),
        (1, '男'),
    )
    sex = models.SmallIntegerField(choices=sex_choices, default=0)
    email = models.EmailField(max_length=64)
    phone = models.IntegerField()
    position = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Role(models.Model):
    """角色表"""
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.caption


class User2Role(models.Model):
    """用户和角色权限对应表，多对多关系"""
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    r = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '用户分配角色'
        unique_together = ('u', 'r')

    def __str__(self):
        return "%s-%s" %(self.u.username, self.r.caption)


class Menu(models.Model):
    """菜单表"""
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='p',null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '菜单表'

    def __str__(self):
        return "%s" % (self.caption,)


class Permission(models.Model):
    """权限表"""
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    icon = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu,null=True,blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'URL权限表'

    def __str__(self):
        return "%s-%s" % (self.caption, self.url)


class Permission2Role(models.Model):
    """角色对权限，多对多，由于为内部运维工具，不再细化到增删改查粒度，只到URL的权限控制粒度"""
    p = models.ForeignKey(Permission, on_delete=models.CASCADE)
    r = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '角色分配权限'
        unique_together = ('p', 'r')

    def __str__(self):
        return "%s==>%s" %(self.r.caption, self.p,)


######################工单管理########################
class Projects(models.Model):
    """项目列表，比如招行项目，兴业项目"""
    project_name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = '项目列表'

    def __str__(self):
        return "%s" % (self.project_name,)


class Envlists(models.Model):
    """各个环境列表（比如测试环境，生产环境等）"""
    env = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = '环境列表'

    def __str__(self):
        return "%s" % (self.env,)


class Workorders(models.Model):
    """工单管理表"""
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    detail = models.TextField()
    project_name = models.ForeignKey(Projects, on_delete=models.CASCADE)
    env_label = models.ForeignKey(Envlists, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    handler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='h', null=True, blank=True)
    handler_role_status = (
        (1, '运维工程师'),
        (2, '测试工程师'),
        (3, '开发工程师'),
        (4, '无'),
    )
    handler_role = models.IntegerField(choices=handler_role_status, default=1)
    handle_time = models.DateTimeField(null=True, blank=True)
    handle_status_choices = (
        (1, '未处理'),
        (2, '处理中'),
        (3, '已处理'),
        (4, '废单'),
    )
    handle_status = models.IntegerField(choices=handle_status_choices, default=1)
    ops_result = models.TextField(null=True, blank=True)
    test_result = models.TextField(null=True, blank=True)
    role_status_choices = (
        (1, '开发工程师'),
        (2, '运维工程师'),
        (3, '测试工程师'),
    )
    role_status = models.IntegerField(choices=role_status_choices, default=1)

    class Meta:
        verbose_name_plural = '工单列表'

    def __str__(self):
        return "%s" % (self.title,)


######################资产管理########################
class IDC(models.Model):
    """机房信息"""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'IDC机房'

    def __str__(self):
        return "%s" % (self.name,)


class Host(models.Model):
    """存储主机列表"""
    hostname = models.CharField(max_length=64,unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey("IDC", on_delete=models.CASCADE)
    assets_type_choices = (
        (1, '虚拟机'),
        (2, '交换机'),
        (3, '服务器'),
        (4, '防火墙'),
    )
    assets_type = models.SmallIntegerField(choices=assets_type_choices, default=1)
    project_name = models.ForeignKey("Projects", on_delete=models.CASCADE)
    env_type = models.ForeignKey("Envlists", on_delete=models.CASCADE)
    cpu = models.CharField(max_length=32)
    disk = models.CharField(max_length=32)
    memory = models.CharField(max_length=32)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name_plural = '主机列表'

