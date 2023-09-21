
class ZHUtil:

    # 只保留 浏览数据
    @staticmethod
    def getVisitCount(visitCountRaw):
        # print(visitCountRaw)

        pos1 = visitCountRaw.index("浏览")
        visitCountStr = (str(visitCountRaw))[0:pos1]

        if ("万" in visitCountStr):
            pos2 = visitCountStr.index("万")
            realVisitCount = (str(visitCountStr))[0:pos2-1]
            # print(realVisitCount)
            # print(type(realVisitCount))
            return str(int(float(realVisitCount)*10000))

        return visitCountStr


    # 把含有 "万"字的  转换为  实际数字
    def caculateRealVisitCount(visitCount):
        if("万" in visitCount):
            pos = visitCount.index("万")
            visitCountStr =  (str(visitCount))[0:pos]

            return int(visitCountStr)*10000

